#!/usr/bin/env python3
"""Read-only checks for the KubeFacet identity migration."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / ".walden/specs/project-identity-rename"
TOKEN = "".join(("kube", "seer"))
OLD_NAME = re.compile(re.escape(TOKEN), re.IGNORECASE)
HEX_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
STABLE_VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
EXPECTED_HISTORY_RECORDS = 98


class VerificationError(Exception):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(message: str) -> None:
    raise VerificationError(message)


def chart_field(chart_text: str, field: str) -> str:
    pattern = re.compile(rf"^{re.escape(field)}:\s*(.*?)\s*(?:#.*)?$")
    values = [match.group(1).strip().strip("\"'") for line in chart_text.splitlines() if (match := pattern.fullmatch(line))]
    if len(values) != 1 or not values[0]:
        fail(f"expected exactly one non-empty root {field} in charts/kubefacet/Chart.yaml")
    return values[0]


def has_release_note_sections(note: str) -> bool:
    section = ""
    found = {"Highlights": False, "Upgrade considerations": False}
    for line in note.splitlines():
        heading = re.fullmatch(r"##\s+(.+?)\s*", line)
        if heading:
            section = heading.group(1)
        elif section in found and re.match(r"^\s*[-*]\s+", line) and len(line) > 22:
            found[section] = True
    return all(found.values())


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")


def safe_relative(value: str) -> str:
    if not isinstance(value, str) or not value:
        fail("empty or invalid relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        fail(f"unsafe relative path: {value!r}")
    return path.as_posix()


def git_blob(root: Path, commit: str, relative: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "show", f"{commit}:{relative}"],
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        fail(f"cannot read baseline blob {relative!r}: {exc.stderr.decode(errors='replace').strip()}")


def validate_history(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    records = read_json(root / ".walden/specs/project-identity-rename/historical-identity-records.json")
    baseline = read_json(root / ".walden/specs/project-identity-rename/api-schema-baseline.json")
    if records.get("schema_version") != 1 or baseline.get("schema_version") != 1:
        fail("unsupported historical identity data version")
    commit = records.get("baseline_commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40,64}", commit):
        fail("invalid historical baseline commit")
    if baseline.get("baseline_commit") != commit:
        fail("identity and API baselines refer to different commits")
    try:
        subprocess.check_call(
            ["git", "-C", str(root), "cat-file", "-e", f"{commit}^{{commit}}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        fail(f"baseline commit is unavailable: {commit}")

    entries = records.get("records")
    if not isinstance(entries, list) or len(entries) != EXPECTED_HISTORY_RECORDS:
        fail(f"expected {EXPECTED_HISTORY_RECORDS} individually preserved historical records")
    by_path: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            fail("invalid historical record")
        relative = safe_relative(entry.get("path"))
        sha = entry.get("sha256")
        lines = entry.get("lines")
        if not isinstance(sha, str) or not HEX_SHA256.fullmatch(sha):
            fail(f"invalid historical digest for {relative}")
        if not isinstance(lines, list) or any(type(line) is not int or line < 1 for line in lines):
            fail(f"invalid historical line inventory for {relative}")
        if lines != sorted(set(lines)):
            fail(f"historical line inventory is not unique and ordered for {relative}")
        if relative in by_path:
            fail(f"duplicate historical record for {relative}")
        path = root / relative
        try:
            current = path.read_bytes()
        except OSError as exc:
            fail(f"preserved historical file is missing: {relative}: {exc}")
        original = git_blob(root, commit, relative)
        if digest(original) != sha or digest(current) != sha or current != original:
            fail(f"preserved historical bytes changed: {relative}")
        matching_lines = [
            line_no
            for line_no, line in enumerate(current.splitlines(keepends=True), 1)
            if OLD_NAME.search(line.decode("utf-8", errors="replace"))
        ]
        if matching_lines != lines:
            fail(f"historical occurrence inventory changed: {relative}")
        by_path[relative] = entry

    resources = baseline.get("resources")
    if not isinstance(resources, dict) or set(resources) != {"facet", "access-policy"}:
        fail("the API baseline must contain exactly the two reviewed resources")
    for name, resource in resources.items():
        if not isinstance(resource, dict):
            fail(f"invalid API baseline entry for {name}")
        relative = safe_relative(resource.get("source_path"))
        sha = resource.get("sha256")
        encoded = resource.get("content_b64")
        if not isinstance(sha, str) or not HEX_SHA256.fullmatch(sha) or not isinstance(encoded, str):
            fail(f"invalid API baseline digest or content for {name}")
        try:
            snapshot = base64.b64decode(encoded, validate=True)
        except (ValueError, base64.binascii.Error):
            fail(f"invalid API baseline encoding for {name}")
        original = git_blob(root, commit, relative)
        if digest(snapshot) != sha or original != snapshot:
            fail(f"API baseline provenance mismatch for {name}")
    return records, baseline


def decode_path(value: Any) -> str:
    if not isinstance(value, str):
        fail("encoded exception path is not text")
    try:
        decoded = base64.b64decode(value, validate=True).decode("utf-8")
    except (ValueError, UnicodeError, base64.binascii.Error):
        fail("invalid encoded exception path")
    return safe_relative(decoded)


def load_exceptions(root: Path, records: dict[str, Any]) -> tuple[dict, dict]:
    data = read_json(root / ".walden/specs/project-identity-rename/identity-exceptions.json")
    if data.get("schema_version") != 1 or data.get("baseline_commit") != records.get("baseline_commit"):
        fail("identity exception policy version or baseline does not match")
    text_data = data.get("text_exceptions")
    path_data = data.get("path_exceptions")
    if not isinstance(text_data, list) or not isinstance(path_data, list):
        fail("identity exception policy must contain text and path exception lists")
    text_exceptions: dict[tuple[str, int], dict[str, Any]] = {}
    path_exceptions: dict[str, dict[str, Any]] = {}
    for entry in text_data:
        if not isinstance(entry, dict):
            fail("invalid text exception")
        relative = decode_path(entry.get("path_b64"))
        line = entry.get("line")
        sha = entry.get("sha256")
        count = entry.get("count")
        reason = entry.get("reason")
        if type(line) is not int or line < 1 or not isinstance(sha, str) or not HEX_SHA256.fullmatch(sha):
            fail(f"invalid text exception selector for {relative}")
        if type(count) is not int or count < 1 or not isinstance(reason, str) or not reason.strip():
            fail(f"invalid text exception classification for {relative}:{line}")
        if OLD_NAME.search(reason):
            fail(f"exception reason repeats an obsolete identifier for {relative}:{line}")
        key = (relative, line)
        if key in text_exceptions:
            fail(f"duplicate text exception selector for {relative}:{line}")
        text_exceptions[key] = {"sha256": sha, "count": count, "reason": reason}
    for entry in path_data:
        if not isinstance(entry, dict):
            fail("invalid path exception")
        relative = decode_path(entry.get("path_b64"))
        sha = entry.get("sha256")
        reason = entry.get("reason")
        if not OLD_NAME.search(relative):
            fail(f"path exception does not identify an obsolete path: {relative}")
        if not isinstance(sha, str) or not HEX_SHA256.fullmatch(sha) or not isinstance(reason, str) or not reason.strip():
            fail(f"invalid path exception classification for {relative}")
        if OLD_NAME.search(reason):
            fail(f"path exception reason repeats an obsolete identifier for {relative}")
        if relative in path_exceptions:
            fail(f"duplicate path exception selector for {relative}")
        path_exceptions[relative] = {"sha256": sha, "reason": reason}
    return text_exceptions, path_exceptions


def source_paths(root: Path) -> list[str]:
    try:
        listed = subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
        )
        paths = {safe_relative(item.decode("utf-8")) for item in listed.split(b"\0") if item}
    except (subprocess.CalledProcessError, UnicodeError):
        paths = {
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.relative_to(root).parts
        }
    return sorted(path for path in paths if (root / path).is_file() or (root / path).is_symlink())


def scan_tree(
    root: Path,
    files: list[str],
    historical: dict[str, dict[str, Any]],
    text_exceptions: dict[tuple[str, int], dict[str, Any]],
    path_exceptions: dict[str, dict[str, Any]],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    classified: list[str] = []
    used_text: set[tuple[str, int]] = set()
    used_paths: set[str] = set()
    for relative in files:
        path = root / relative
        try:
            raw = path.read_bytes()
        except OSError as exc:
            errors.append(f"cannot read {relative}: {exc}")
            continue
        file_sha = digest(raw)
        if OLD_NAME.search(relative):
            historic = historical.get(relative)
            path_entry = path_exceptions.get(relative)
            if historic and historic.get("sha256") == file_sha:
                classified.append(f"historical path {relative} sha256={file_sha}")
            elif path_entry and path_entry.get("sha256") == file_sha:
                used_paths.add(relative)
                classified.append(f"migration path {relative} sha256={file_sha}: {path_entry['reason']}")
            else:
                errors.append(f"unclassified identity path {relative}")

        if b"\0" in raw:
            continue
        try:
            raw.decode("utf-8")
        except UnicodeError:
            continue
        for line_no, line in enumerate(raw.splitlines(keepends=True), 1):
            try:
                line_text = line.decode("utf-8")
            except UnicodeError:
                continue
            matches = list(OLD_NAME.finditer(line_text))
            if not matches:
                continue
            found = [match.group() for match in matches]
            historic = historical.get(relative)
            if historic and historic.get("sha256") == file_sha:
                if line_no not in historic.get("lines", []):
                    errors.append(f"historical line inventory mismatch {relative}:{line_no}")
                else:
                    classified.append(f"historical {relative}:{line_no} count={len(matches)} sha256={digest(line)}")
                continue
            key = (relative, line_no)
            expected = text_exceptions.get(key)
            if expected and expected.get("sha256") == digest(line) and expected.get("count") == len(matches):
                used_text.add(key)
                classified.append(
                    f"migration {relative}:{line_no} count={len(matches)} sha256={digest(line)}: {expected['reason']}"
                )
            else:
                errors.append(f"unclassified text {relative}:{line_no} matches={found!r}")

    for key, entry in text_exceptions.items():
        if key not in used_text:
            errors.append(f"stale text exception {key[0]}:{key[1]} sha256={entry['sha256']}")
    for relative, entry in path_exceptions.items():
        if relative not in used_paths:
            errors.append(f"stale path exception {relative} sha256={entry['sha256']}")
    return classified, errors


def run_history() -> None:
    records, baseline = validate_history(ROOT)
    print(
        "PROJECT_IDENTITY=history STATUS=passed "
        f"records={len(records['records'])} baseline_resources={len(baseline['resources'])}"
    )


def run_docs() -> None:
    old_title = TOKEN.capitalize()
    old_module = f"github.com/steeltanuki/{TOKEN}"
    old_group = f"{TOKEN}.io"
    migration_path = f"docs/migration-from-{TOKEN}.md"
    old_api_feature = f"{TOKEN}-api-foundation"
    required: dict[str, tuple[str, ...]] = {
        "README.md": (
            "**Declarative, typed views and aggregations over Kubernetes resources.**",
            "Define a `Facet` custom resource",
            "KubeFacet continuously evaluates the selected resources",
            "kind: Facet",
            migration_path,
            "--version 0.2.1",
        ),
        "CONTRIBUTING.md": (
            "Walden is optional for contributors",
            "ordinary issue or pull request",
            "maintainer decides whether a new or updated specification is needed",
            ".walden/current-identity.md",
        ),
        "SPECIFICATIONS.md": (
            ".walden/current-identity.md",
            f"    {old_api_feature}/",
            "`Facet` Custom Resource",
            "kind: FacetAccessPolicy",
        ),
        "docs/api-reference.md": (
            "`Facet`, a namespaced declaration",
            "`FacetAccessPolicy`, a cluster-scoped singleton",
            "kind: Facet",
            "kind: FacetAccessPolicy",
        ),
        ".walden/constitution.md": (
            "current-identity.md",
            "`Facet` and `FacetAccessPolicy`",
            "1.35.6",
            "1.36.2",
        ),
        ".walden/current-identity.md": (
            "supersedes only their project, API, packaging, telemetry,",
            f"`{old_api_feature}`",
            "`installation-access-policy`",
            "`admission-validation`",
            "`observability`",
            "`packaging-and-installation`",
            "`end-to-end-scenarios`",
            "`local-development-environment`",
            "`local-cluster-resume`",
            "`release-distribution`",
            "requirements remain in force",
            "selected-feature evidence",
        ),
        migration_path: (
            "v0.1.x to KubeFacet v0.2.0",
            f"`{old_title}` namespaced custom resource | `Facet`",
            f"`{old_title}AccessPolicy` cluster-scoped custom resource | `FacetAccessPolicy`",
            f"`{old_group}/v1alpha1` | `kubefacet.steeltanuki.it/v1alpha1`",
            f"`{old_module}` | `github.com/steeltanuki/kubefacet`",
            f"`{TOKEN.upper()}_` environment settings",
            f"`{TOKEN}_` Prometheus metrics",
            "A Helm upgrade\nacross this boundary is unsupported.",
            "no CRD conversion webhook",
            f"https://github.com/steeltanuki/{TOKEN}/blob/v0.1.6/docs/installation.md",
            f"https://github.com/steeltanuki/{TOKEN}/blob/v0.1.6/hack/uninstall-{TOKEN}.sh",
            "Rename the GitHub repository",
            "Update the maintainer's local Git remote",
            "Review the GitHub description, topics, and social preview image",
            "Confirm GHCR image and chart package ownership",
            "Publish KubeFacet v0.2.0 later",
            "Register the project with Artifact Hub later",
        ),
        "docs/installation.md": (
            migration_path.split("/", 1)[1],
            "does not create the release tag or",
            "--version 0.2.1",
        ),
        "docs/releases/v0.2.0.md": (
            migration_path.split("/", 1)[1],
            "does not create a tag, GitHub Release, image, or chart",
        ),
        "charts/kubefacet/README.md": (
            migration_path,
        ),
        "docs/release-pipeline-audit.md": (
            "Historical report dated 2026-09-25",
            "current KubeFacet installation instructions.",
            "automation remains",
            "a proposal and is not implemented by this migration",
        ),
        ".walden/specs/project-identity-rename/verification-report.md": (
            "## Scope and evidence boundary",
            "## Declared checkpoints and actual outcomes",
            "## Regenerated artifacts",
            "## Repository identity residue",
            "## Commit boundaries",
            "## Manual actions after merge",
            "## Walden delivery checkpoint",
        ),
    }
    contents: dict[str, str] = {}
    for relative, phrases in required.items():
        try:
            content = (ROOT / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            fail(f"current migration documentation is missing or unreadable: {relative}: {exc}")
        contents[relative] = content
        for phrase in phrases:
            if phrase not in content:
                fail(f"current documentation contract is missing from {relative}: {phrase!r}")

    if "kind: KubeFacet" in contents["README.md"] or "kind: KubeFacet" in contents["docs/api-reference.md"]:
        fail("current API examples must use the Facet Kind")
    for relative in ("README.md", "docs/installation.md", "docs/releases/v0.2.0.md"):
        if migration_path.split("/", 1)[1] not in contents.get(relative, (ROOT / relative).read_text(encoding="utf-8")):
            fail(f"current entry point does not link the migration guide: {relative}")

    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    if "./hack/verify-project-identity.sh audit" not in makefile:
        fail("make verify does not run the whole-repository identity audit")
    if "./hack/verify-project-identity.sh audit" not in ci:
        fail("CI does not run the identity audit on the documentation-only path")
    print(f"PROJECT_IDENTITY=docs STATUS=passed files={len(required)}")


def run_api() -> None:
    validate_history(ROOT)
    env = os.environ.copy()
    env.setdefault("GOCACHE", "/tmp/kubefacet-go-build")
    try:
        result = subprocess.run(
            ["go", "run", "./hack/identity-schema"],
            cwd=ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        fail(f"cannot run the API schema comparison: {exc}")
    if result.returncode != 0:
        fail(f"API schema comparison failed:\n{result.stdout}")
    print(result.stdout, end="")


def run_builds() -> None:
    env = os.environ.copy()
    env.setdefault("GOCACHE", "/tmp/kubefacet-go-build")
    commands = (
        ("./cmd/kubefacet", "kubefacet"),
        ("./cmd/kubefacet-local", "kubefacet-local"),
        ("./cmd/kubefacet-purge", "kubefacet-purge"),
    )
    with tempfile.TemporaryDirectory(prefix="kubefacet-build-") as temp:
        for package, binary in commands:
            output = Path(temp) / binary
            try:
                result = subprocess.run(
                    ["go", "build", "-trimpath", "-o", str(output), package],
                    cwd=ROOT,
                    env=env,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=False,
                )
            except OSError as exc:
                fail(f"cannot build {binary}: {exc}")
            if result.returncode != 0 or not output.is_file():
                fail(f"build of {binary} failed:\n{result.stdout}")
    print("PROJECT_IDENTITY=builds STATUS=passed BINARIES=3")


def run_runtime() -> None:
    contracts = {
        "internal/managerapp/application.go": (
            'DefaultWebhookCertDir             = "/var/run/secrets/kubefacet/webhook"',
            'DefaultWebhookCAFile              = "/var/run/secrets/kubefacet/ca/ca.crt"',
            'DefaultLeaderElectionNamespace    = "kubefacet-system"',
            'DefaultLeaderElectionID           = "kubefacet-controller"',
            '"kubefacet-webhook.kubefacet-system.svc.cluster.local"',
        ),
        "internal/managerapp/lifecycle.go": (
            'ValidatingWebhookName         = "kubefacet-validating-webhook"',
            'DefaultWebhookServiceName     = "kubefacet-webhook"',
            'DefaultDeploymentName         = "kubefacet"',
            '"/validate-kubefacet-steeltanuki-it-v1alpha1-facet"',
            '"/validate-kubefacet-steeltanuki-it-v1alpha1-facetaccesspolicy"',
        ),
        "internal/admission/webhook.go": (
            'FacetWebhookPath = "/validate-kubefacet-steeltanuki-it-v1alpha1-facet"',
            'FacetAccessPolicyWebhookPath = "/validate-kubefacet-steeltanuki-it-v1alpha1-facetaccesspolicy"',
            'validatingWebhookConfigurationName = "kubefacet-validating-webhook"',
            'facetWebhookName                   = "facet.kubefacet.steeltanuki.it"',
        ),
        "internal/reconciliation/setup.go": (
            'controllerName = "kubefacet-reconciliation-runtime"',
            "mgr.GetEventRecorderFor(controllerName)",
        ),
        "internal/purge/purge.go": (
            'ConfirmationToken   = "purge-kubefacet-crds"',
            'FacetCRDName        = "facets.kubefacet.steeltanuki.it"',
            'AccessPolicyCRDName = "facetaccesspolicies.kubefacet.steeltanuki.it"',
        ),
        "internal/managerapp/version.go": ('return "kubefacet version="',),
        "cmd/kubefacet/main.go": (
            'usage: kubefacet package ',
            '"expected-facet-crd-storage-version"',
        ),
        "internal/localprobe/probe.go": (
            'LabelSelector: "app.kubernetes.io/name=kubefacet"',
            'Get(ctx, "kubefacet-validating-webhook"',
        ),
        "test/e2e/session.go": ('Get(ctx, "kubefacet-validating-webhook"',),
        "hack/verify-admission-boundaries.sh": (
            "second Facet API version",
            'Group: "kubefacet.steeltanuki.it"',
        ),
    }
    for relative, snippets in contracts.items():
        try:
            content = (ROOT / relative).read_text(encoding="utf-8")
        except OSError as exc:
            fail(f"cannot read runtime identity contract {relative}: {exc}")
        for snippet in snippets:
            if snippet not in content:
                fail(f"runtime identity is missing from {relative}: {snippet!r}")
    print(f"PROJECT_IDENTITY=runtime STATUS=passed contracts={len(contracts)}")


def run_observability() -> None:
    metric_names = (
        "kubefacet_reconciliations_total",
        "kubefacet_reconciliation_duration_seconds",
        "kubefacet_resources_read_total",
        "kubefacet_source_failures_total",
        "kubefacet_results_produced_total",
        "kubefacet_status_updates_total",
        "kubefacet_authorization_decisions_total",
        "kubefacet_jsonpath_failures_total",
        "kubefacet_source_watch_restarts_total",
    )
    contracts = {
        "internal/observability/metrics.go": metric_names,
        "internal/localprobe/probe.go": metric_names,
        "test/integration/observability_core_test.go": metric_names,
        "hack/verify-observability-boundaries.sh": metric_names,
        "test/e2e/observability_scenario.go": ("kubefacet_status_updates_total",),
        "test/integration/observability_runtime_test.go": (
            '"kubefacet.reconciliation"',
            '"kubefacet.reconciliation."',
        ),
        "internal/observability/observer.go": (
            '"kubefacet.reconciliation"',
            '"kubefacet.namespace"',
            '"kubefacet.attempt_id"',
            '"kubefacet.stage"',
            '"kubefacet.outcome"',
        ),
        "test/integration/installation_access_policy_test.go": (
            't.Run("ProjectIdentityObservability"',
        ),
    }
    for relative, snippets in contracts.items():
        try:
            content = (ROOT / relative).read_text(encoding="utf-8")
        except OSError as exc:
            fail(f"cannot read observability identity contract {relative}: {exc}")
        for snippet in snippets:
            if snippet not in content:
                fail(f"observability identity is missing from {relative}: {snippet!r}")
    old_metric = re.compile(r"\b" + re.escape(TOKEN) + r"_(?:reconciliations_total|reconciliation_duration_seconds|resources_read_total|source_failures_total|results_produced_total|status_updates_total|authorization_decisions_total|jsonpath_failures_total|source_watch_restarts_total)\b")
    for relative in contracts:
        content = (ROOT / relative).read_text(encoding="utf-8")
        if old_metric.search(content):
            fail(f"obsolete metric family remains in {relative}")
    print("PROJECT_IDENTITY=observability STATUS=passed METRIC_FAMILIES=9")


def run_package() -> None:
    chart_dir = ROOT / "charts/kubefacet"
    chart_file = chart_dir / "Chart.yaml"
    values_file = chart_dir / "values.yaml"
    chart_text = chart_file.read_text(encoding="utf-8")
    values_text = values_file.read_text(encoding="utf-8")
    required_metadata = (
        "name: kubefacet",
        "description: Kubernetes operator for building typed, aggregated views of Kubernetes resources across namespaces",
        'kubeVersion: ">=1.35.0-0 <1.37.0-0"',
        "  - kubernetes\n  - operator\n  - aggregation\n  - custom-resources\n  - resource-views",
        "https://github.com/steeltanuki/kubefacet",
    )
    for snippet in required_metadata:
        if snippet not in chart_text:
            fail(f"Helm chart metadata is missing {snippet!r}")
    chart_version = chart_field(chart_text, "version")
    chart_app_version = chart_field(chart_text, "appVersion")
    if not STABLE_VERSION.fullmatch(chart_version) or chart_app_version != chart_version:
        fail("Helm chart version and appVersion must match a stable SemVer release")
    if "repository: ghcr.io/steeltanuki/kubefacet" not in values_text:
        fail("Helm manager image repository does not use KubeFacet identity")
    if "webhookCertDir: /var/run/secrets/kubefacet/webhook" not in values_text:
        fail("Helm serving-certificate path does not use KubeFacet identity")
    crd_names = (
        "kubefacet.steeltanuki.it_facets.yaml",
        "kubefacet.steeltanuki.it_facetaccesspolicies.yaml",
    )
    for name in crd_names:
        source = ROOT / "config/crd/bases" / name
        packaged = chart_dir / "crds" / name
        if not source.is_file() or not packaged.is_file() or source.read_bytes() != packaged.read_bytes():
            fail(f"packaged CRD is missing or differs from generated source: {name}")
    historical_records, _ = validate_history(ROOT)
    text_exceptions, _ = load_exceptions(ROOT, historical_records)
    files = [path for path in chart_dir.rglob("*") if path.is_file()]
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if OLD_NAME.search(relative):
            fail(f"Helm chart path retains an obsolete project identity: {relative}")
        raw = path.read_bytes()
        try:
            content = raw.decode("utf-8")
        except UnicodeError:
            continue
        for line_number, line in enumerate(content.splitlines(keepends=True), 1):
            matches = list(OLD_NAME.finditer(line))
            if not matches:
                continue
            expected = text_exceptions.get((relative, line_number))
            if expected and expected.get("sha256") == digest(line.encode("utf-8")) and expected.get("count") == len(matches):
                continue
            fail(f"Helm chart retains an obsolete project identity: {relative}:{line_number}")
    helpers = (chart_dir / "templates/_helpers.tpl").read_text(encoding="utf-8")
    if 'define "kubefacet.labels"' not in helpers or 'define "kubefacet.selectorLabels"' not in helpers:
        fail("Helm helper namespace is incomplete")
    if 'app.kubernetes.io/name=kubefacet' not in (ROOT / "internal/localprobe/probe.go").read_text(encoding="utf-8"):
        fail("runtime readiness selector does not match the chart workload")
    print(f"PROJECT_IDENTITY=package STATUS=passed CRDS={len(crd_names)}")


def run_release() -> None:
    release_script = (ROOT / "hack/release-distribution.sh").read_text(encoding="utf-8")
    release_tests = (ROOT / "hack/test-release-distribution.sh").read_text(encoding="utf-8")
    workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    ordinary_ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    first_release_note = (ROOT / "docs/releases/v0.2.0.md").read_text(encoding="utf-8")
    contracts = {
        "hack/release-distribution.sh": (
            'readonly repository="steeltanuki/kubefacet"',
            'expected_image="ghcr.io/steeltanuki/kubefacet:$version"',
            'chart_ref="oci://$(registry_host)/steeltanuki/charts/kubefacet"',
            'chart_url="oci://ghcr.io/steeltanuki/charts/kubefacet"',
            'local chart="$root/charts/kubefacet/Chart.yaml"',
            'if ! grep -Fqx "# KubeFacet $tag" "$note_file"',
            '[[ "${GITHUB_REF_PROTECTED:-}" == true ]]',
            '"${GITHUB_EVENT_NAME:-}" == push',
        ),
        ".github/workflows/release.yml": (
            'group: kubefacet-release-${{ github.ref }}',
            'tags:\n      - "v*"',
            'packages: write',
            'RELEASE_GATE_SOURCE_SHA',
            'kubefacet-release-candidate',
        ),
        "hack/test-release-distribution.sh": (
            'name: kubefacet',
            'GITHUB_REPOSITORY=steeltanuki/kubefacet',
            'version: 0.2.0',
            'ghcr.io/steeltanuki/kubefacet:0.2.0',
            'oci://ghcr.io/steeltanuki/charts/kubefacet',
        ),
    }
    sources = {
        "hack/release-distribution.sh": release_script,
        ".github/workflows/release.yml": workflow,
        "hack/test-release-distribution.sh": release_tests,
    }
    for relative, snippets in contracts.items():
        for snippet in snippets:
            if snippet not in sources[relative]:
                fail(f"release identity or safety contract is missing from {relative}: {snippet!r}")
        if OLD_NAME.search(sources[relative]):
            fail(f"release infrastructure retains an obsolete operational identifier: {relative}")
    if re.search(r"packages:\s*write", ordinary_ci):
        fail("ordinary CI must not receive package publication permission")
    chart = (ROOT / "charts/kubefacet/Chart.yaml").read_text(encoding="utf-8")
    version = chart_field(chart, "version")
    app_version = chart_field(chart, "appVersion")
    if not STABLE_VERSION.fullmatch(version) or app_version != version:
        fail("the chart version and appVersion must match a stable SemVer release")
    tag = f"v{version}"
    current_note_path = ROOT / "docs/releases" / f"{tag}.md"
    try:
        current_release_note = current_note_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"maintainer release notes are missing or unreadable for {tag}: {exc}")
    if f"# KubeFacet {tag}" not in current_release_note.splitlines():
        fail(f"maintainer release notes must identify {tag} in the title")
    if re.search(r"(^|[^A-Za-z])(TODO|TBD|PLACEHOLDER|FILL\s+IN)([^A-Za-z]|$)", current_release_note, re.IGNORECASE):
        fail(f"maintainer release notes for {tag} contain unfinished placeholder text")
    if not has_release_note_sections(current_release_note):
        fail(f"maintainer release notes for {tag} need substantive Highlights and Upgrade considerations sections")
    for snippet in (
        "# KubeFacet v0.2.0",
        "ghcr.io/steeltanuki/kubefacet:0.2.0",
        "oci://ghcr.io/steeltanuki/charts/kubefacet",
        "Upgrade considerations",
    ):
        if snippet not in first_release_note:
            fail(f"v0.2.0 release metadata is missing {snippet!r}")
    print(f"PROJECT_IDENTITY=release STATUS=passed VERSION={version} IMAGE=ghcr.io/steeltanuki/kubefacet CHART=kubefacet")


def active_identity_files() -> list[Path]:
    paths: set[Path] = set()
    for relative in ("Makefile", "cmd", "config", "examples", "hack", "internal", "test"):
        base = ROOT / relative
        if base.is_file():
            paths.add(base)
        elif base.is_dir():
            paths.update(path for path in base.rglob("*") if path.is_file())
    return sorted(path for path in paths if path != Path(__file__).resolve() and "__pycache__" not in path.parts)


def run_environment() -> None:
    files = active_identity_files()
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if OLD_NAME.search(relative):
            fail(f"active environment/runtime path retains an obsolete identity: {relative}")
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        if OLD_NAME.search(content):
            fail(f"active environment/runtime source retains an obsolete identity: {relative}")
    contracts = {
        "cmd/kubefacet/main.go": (
            'os.Getenv("KUBEFACET_RELEASE_NAME")',
            'os.Getenv("KUBEFACET_RELEASE_NAMESPACE")',
        ),
        "internal/managerapp/lifecycle.go": ('env.Name == "KUBEFACET_VERSION"',),
        "internal/localprobe/probe.go": (
            'os.Getenv("KUBEFACET_LOCAL_READYZ_URL")',
            'os.Getenv("KUBEFACET_LOCAL_METRICS_URL")',
            'os.Getenv("KUBEFACET_LOCAL_KIND_VERSION")',
            'os.Getenv("KUBEFACET_LOCAL_HELM_VERSION")',
        ),
        "test/e2e/session.go": (
            'os.Getenv("KUBEFACET_E2E_KUBECONFIG")',
            'os.Getenv("KUBEFACET_E2E_SOURCE_IDENTITY")',
        ),
        "hack/test-package-compatibility.sh": (
            'config_var="KUBEFACET_PACKAGE_KUBECONFIG_${version//./_}"',
            'context_var="KUBEFACET_PACKAGE_CONTEXT_${version//./_}"',
        ),
        "hack/local-environment-acceptance.sh": (
            "KUBEFACET_TEST_PODMAN_FAIL_START",
            "KUBEFACET_TEST_KIND_FAIL_CREATE",
            "KUBEFACET_TEST_HELM_FAIL_INSTALL",
        ),
        "hack/e2e-harness-acceptance.sh": (
            "KUBEFACET_TEST_KIND_FAIL_CREATE",
            "KUBEFACET_TEST_PODMAN_FAIL_BUILD",
            "KUBEFACET_FAIL_READY_PORT_FORWARD",
        ),
        "hack/envtest-assets.sh": (
            "/kubefacet/envtest",
            "/kubefacet-envtest.",
        ),
        "Makefile": (
            "/tmp/kubefacet-e2e-go-build",
            "/tmp/kubefacet-e2e-go-mod",
        ),
    }
    for relative, snippets in contracts.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in content:
                fail(f"environment identity is missing from {relative}: {snippet!r}")
    print(f"PROJECT_IDENTITY=environment STATUS=passed SOURCES={len(files)}")


def run_local() -> None:
    catalog = (ROOT / "examples/catalog.txt").read_text(encoding="utf-8")
    examples = [line.split("#", 1)[0].strip() for line in catalog.splitlines()]
    examples = [name for name in examples if name]
    expected_examples = (
        "builtin-resource",
        "typed-extraction",
        "value-operator",
        "cross-namespace-aggregation",
        "custom-resource",
        "authorization-denial",
        "partial-degradation",
    )
    if tuple(examples) != expected_examples:
        fail("the seven-example catalog changed while migrating its identities")
    local = (ROOT / "hack/local-environment.sh").read_text(encoding="utf-8")
    toolchain = (ROOT / "hack/toolchain.mk").read_text(encoding="utf-8")
    local_examples = (ROOT / "hack/local-examples.sh").read_text(encoding="utf-8")
    local_values = (ROOT / "config/local/values.yaml").read_text(encoding="utf-8")
    contracts = {
        "hack/local-environment.sh": (
            'KUBEFACET_LOCAL_CLUSTER_NAME:-kubefacet-local',
            'KUBEFACET_LOCAL_KUBE_CONTEXT:-kind-kubefacet-local',
            'KUBEFACET_LOCAL_NAMESPACE:-kubefacet-system',
            'KUBEFACET_LOCAL_RELEASE:-kubefacet',
            'KUBEFACET_LOCAL_PROVIDER:-podman',
            'requires the Podman provider',
            '}/kubefacet/local',
            '}/kubefacet/local',
        ),
        "hack/toolchain.mk": (
            "KUBEFACET_LOCAL_CLUSTER_NAME ?= kubefacet-local",
            "KUBEFACET_LOCAL_KUBE_CONTEXT ?= kind-kubefacet-local",
            "KUBEFACET_LOCAL_NAMESPACE ?= kubefacet-system",
            "KUBEFACET_LOCAL_RELEASE ?= kubefacet",
            "KUBEFACET_LOCAL_PROVIDER ?= podman",
        ),
        "hack/local-examples.sh": (
            'facet.yaml',
            'get facet -l "$NAMESPACE_LABEL=$name"',
            "kubefacet.steeltanuki.it/example",
            "fixtures.kubefacet.steeltanuki.it",
        ),
        "hack/e2e-harness.sh": (
            'charts/kubefacet',
            'kind: Facet',
            'kubefacet-e2e-',
            'kubefacet-validating-webhook',
            'kubefacet-system',
        ),
        "hack/verify-local-environment.sh": (
            '"$directory/facet.yaml"',
            'kubefacet-e2e-',
        ),
        "internal/localprobe/probe.go": (
            'app.kubernetes.io/name=kubefacet',
            'kubefacet-validating-webhook',
        ),
    }
    contents = {
        "hack/local-environment.sh": local,
        "hack/toolchain.mk": toolchain,
        "hack/local-examples.sh": local_examples,
        "hack/e2e-harness.sh": (ROOT / "hack/e2e-harness.sh").read_text(encoding="utf-8"),
        "hack/verify-local-environment.sh": (ROOT / "hack/verify-local-environment.sh").read_text(encoding="utf-8"),
        "internal/localprobe/probe.go": (ROOT / "internal/localprobe/probe.go").read_text(encoding="utf-8"),
    }
    for relative, snippets in contracts.items():
        for snippet in snippets:
            if snippet not in contents[relative]:
                fail(f"local identity is missing from {relative}: {snippet!r}")
    for name in expected_examples:
        manifest = ROOT / "examples" / name / "facet.yaml"
        if not manifest.is_file():
            fail(f"renamed Facet example is missing: {name}/facet.yaml")
        content = manifest.read_text(encoding="utf-8")
        if "apiVersion: kubefacet.steeltanuki.it/v1alpha1" not in content or "kind: Facet" not in content:
            fail(f"Facet example has the wrong API identity: {name}/facet.yaml")
    if "kubefacet-example-" not in local_values or "fixtures.kubefacet.steeltanuki.it" not in local_values:
        fail("local chart values do not match the renamed example namespaces and fixture group")
    print(f"PROJECT_IDENTITY=local STATUS=passed EXAMPLES={len(expected_examples)}")


def run_audit() -> None:
    records, _ = validate_history(ROOT)
    historical = {entry["path"]: entry for entry in records["records"]}
    text_exceptions, path_exceptions = load_exceptions(ROOT, records)
    files = source_paths(ROOT)
    classified, errors = scan_tree(ROOT, files, historical, text_exceptions, path_exceptions)
    print(f"PROJECT_IDENTITY_AUDIT occurrences={len(classified)} unclassified={len(errors)} files={len(files)}")
    for item in classified:
        print(f"CLASSIFIED {item}")
    for item in errors[:100]:
        print(f"UNCLASSIFIED {item}", file=sys.stderr)
    if len(errors) > 100:
        print(f"UNCLASSIFIED ... {len(errors) - 100} additional findings", file=sys.stderr)
    if errors:
        fail(f"{len(errors)} unclassified identity residue(s)")
    if not classified:
        fail("the residue scan did not classify any expected historical or migration occurrence")
    print("PROJECT_IDENTITY=audit STATUS=passed")


def run_audit_summary() -> None:
    records, _ = validate_history(ROOT)
    historical = {entry["path"]: entry for entry in records["records"]}
    text_exceptions, path_exceptions = load_exceptions(ROOT, records)
    files = source_paths(ROOT)
    classified, errors = scan_tree(ROOT, files, historical, text_exceptions, path_exceptions)
    if errors:
        fail(f"{len(errors)} unclassified identity residue(s)")
    if not classified:
        fail("the residue scan did not classify any expected historical or migration occurrence")
    print(
        "PROJECT_IDENTITY_AUDIT "
        f"occurrences={len(classified)} unclassified=0 files={len(files)}"
    )


def make_fixture(root: Path) -> tuple[dict, dict, dict]:
    old = TOKEN
    historical_path = "archive/release-record.json"
    historical_line = ("historical release: " + old + " v0.1.6\n").encode()
    historical_bytes = historical_line
    if digest(historical_bytes) != "da0cb4b432c07f216274fef7b1feefa71d96635b9cdff98183a0018e2f13a280":
        fail("historical audit fixture changed unexpectedly")
    mixed_path = "docs/mixed.md"
    mixed_line = ("Historical mapping: " + old.capitalize() + " v0.1.x -> KubeFacet v0.2.0.\n").encode()
    if digest(mixed_line) != "d20c08180d49dc4f0d7dbfd2f06f41a46dcc04ae4ee3e068d0598adc7099ad7b":
        fail("migration audit fixture changed unexpectedly")
    (root / historical_path).parent.mkdir(parents=True, exist_ok=True)
    (root / historical_path).write_bytes(historical_bytes)
    (root / mixed_path).parent.mkdir(parents=True, exist_ok=True)
    (root / mixed_path).write_bytes(mixed_line)
    historical = {
        historical_path: {"sha256": digest(historical_bytes), "lines": [1], "reason": "fixture history"}
    }
    text = {
        (mixed_path, 1): {
            "sha256": digest(mixed_line),
            "count": 1,
            "reason": "fixture migration mapping",
        }
    }
    return historical, text, {}


def expect_rejected(
    root: Path,
    historical: dict,
    text: dict,
    paths: dict,
    name: str,
    prepare,
) -> None:
    case_root = root / name
    case_root.mkdir()
    case_history, case_text, case_paths = make_fixture(case_root)
    prepare(case_root)
    files = [path.relative_to(case_root).as_posix() for path in case_root.rglob("*") if path.is_file()]
    _, errors = scan_tree(case_root, files, case_history, case_text, case_paths)
    if not errors:
        fail(f"audit acceptance failed to reject scenario {name}")


def run_audit_acceptance() -> None:
    with tempfile.TemporaryDirectory(prefix="kubefacet-identity-") as temp:
        root = Path(temp)
        historical, text, paths = make_fixture(root / "positive")
        files = [path.relative_to(root / "positive").as_posix() for path in (root / "positive").rglob("*") if path.is_file()]
        classified, errors = scan_tree(root / "positive", files, historical, text, paths)
        if errors or len(classified) != 2:
            fail(f"audit acceptance positive fixture failed: {errors!r}")

        old = TOKEN
        scenarios = [
            ("obsolete-import", "src/import.go", f'import "github.com/steeltanuki/{old}/api/v1alpha1"\n'),
            ("obsolete-api-group-and-kind", "config/resource.yaml", f"apiVersion: {old}.io/v1alpha1\nkind: {old.capitalize()}\n"),
            ("obsolete-environment", "hack/runtime.sh", f"export {old.upper()}_IMAGE=manager\n"),
            ("obsolete-metric", "internal/metrics.go", f"metric = {old}_reconciliations_total\n"),
            ("obsolete-selector", "charts/operator.yaml", f"app.kubernetes.io/name={old}\n"),
            ("mixed-case", "docs/current.md", f"This active line uses {old[:4].capitalize()}{old[4:].capitalize()}.\n"),
            ("new-walden-contract", ".walden/specs/new-contract/requirements.md", f"The contract names {old}.\n"),
        ]
        for name, relative, content in scenarios:
            def write_case(case_root: Path, relative=relative, content=content) -> None:
                target = case_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")

            expect_rejected(root, historical, text, paths, name, write_case)

        def path_only(case_root: Path) -> None:
            target = case_root / ("src/" + old[:4].capitalize() + old[4:].capitalize() + "/clean.go")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("package clean\n", encoding="utf-8")

        expect_rejected(root, historical, text, paths, "path-only-residue", path_only)

        def changed_allowed_line(case_root: Path) -> None:
            target = case_root / "docs/mixed.md"
            target.write_text("Historical mapping: " + old.capitalize() + " v0.1.x -> KubeFacet v0.2.0 revised.\n", encoding="utf-8")

        expect_rejected(root, historical, text, paths, "changed-allowed-document-line", changed_allowed_line)

        def appended_reference(case_root: Path) -> None:
            target = case_root / "docs/mixed.md"
            with target.open("a", encoding="utf-8") as stream:
                stream.write("An appended active clause names " + old + ".\n")

        expect_rejected(root, historical, text, paths, "appended-reference-to-mixed-document", appended_reference)

        def changed_historical(case_root: Path) -> None:
            target = case_root / "archive/release-record.json"
            target.write_bytes(target.read_bytes() + b"changed\n")

        expect_rejected(root, historical, text, paths, "changed-historical-record", changed_historical)

    print("PROJECT_IDENTITY=audit-acceptance STATUS=passed rejected_scenarios=11 positive_classes=2")


def run_all() -> None:
    checks = (
        run_history,
        run_docs,
        run_api,
        run_builds,
        run_runtime,
        run_observability,
        run_package,
        run_release,
        run_environment,
        run_local,
    )
    for check in checks:
        check()
    run_audit_summary()
    run_audit_acceptance()
    print("PROJECT_IDENTITY=all STATUS=passed")


def git_output(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), *args], text=True, stderr=subprocess.PIPE
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", b"")
        if isinstance(detail, bytes):
            detail = detail.decode("utf-8", errors="replace")
        fail(f"cannot inspect migration commit history: {detail or exc}")


def run_delivery() -> None:
    records, _ = validate_history(ROOT)
    evidence = read_json(ROOT / ".walden/evidence/project-identity-rename.json")
    report_path = SPEC / "verification-report.md"
    try:
        report = report_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read the durable migration verification report: {exc}")

    required_sections = (
        "## Scope and evidence boundary",
        "## Declared checkpoints and actual outcomes",
        "## Regenerated artifacts",
        "## Repository identity residue",
        "## Commit boundaries",
        "## Manual actions after merge",
        "## Walden delivery checkpoint",
    )
    for section in required_sections:
        if section not in report:
            fail(f"verification report is missing section {section!r}")
    if any(marker in report for marker in ("TODO", "TBD", "Record the ", "not yet run")):
        fail("verification report still contains an unfinished placeholder")
    for claim in (
        "selected feature only",
        "not portfolio-wide certification",
        "legacy feature evidence",
        "make verify",
        "make test GO_TEST_FLAGS=-count=1",
        "make test-compatibility GO_TEST_FLAGS=-count=1",
        "make test-package-compatibility",
        "make local-check",
        "make test-local-environment",
        "make test-local-cluster-resume",
        "./hack/test-project-identity-package.sh",
        "make e2e KUBERNETES_VERSION=1.35.6 GO_TEST_FLAGS=-count=1",
        "make e2e KUBERNETES_VERSION=1.36.2 GO_TEST_FLAGS=-count=1",
        "make test-release-distribution SCENARIO=all",
        "PROJECT_IDENTITY=all STATUS=passed",
        "PROJECT_IDENTITY=audit-acceptance STATUS=passed",
        "PROJECT_IDENTITY=delivery STATUS=passed",
        "walden verify project-identity-rename --json",
        "walden release check project-identity-rename --strict --json",
        "Rename the GitHub repository",
        "Update the maintainer's local Git remote",
        "Review the GitHub description, topics, and social preview image",
        "Confirm GHCR image and chart package ownership",
        "Publish KubeFacet v0.2.0 later",
        "Register the project with Artifact Hub later",
        "historical SHA-256 comparison",
        "isolated negative-injection cases",
    ):
        if claim not in report:
            fail(f"verification report is missing required outcome or handoff detail: {claim!r}")

    task_records = evidence.get("tasks")
    if evidence.get("feature") != "project-identity-rename" or not isinstance(task_records, dict):
        fail("selected migration evidence is missing or has an unexpected feature identity")
    expected_task_ids = set(task_records)
    if not expected_task_ids:
        fail("selected migration evidence contains no completed task records")
    outcome_section = report.split("## Declared checkpoints and actual outcomes", 1)[1].split("\n## ", 1)[0]
    for task_id, task in task_records.items():
        # Task 4.7's evidence is written only after this delivery proof succeeds.
        # During a refresh, its previous record can therefore be stale or failed.
        if task_id == "4.7":
            continue
        if not isinstance(task, dict) or task.get("result") != "passed":
            fail(f"required task {task_id} is missing a passing Walden result")
        execution = task.get("execution", {})
        valid_integrity = (
            execution.get("origin") == "complete"
            and execution.get("policy") == "completion-post-state/v1"
            and execution.get("integrity") == "post-state"
        ) or (
            execution.get("origin") == "verify"
            and execution.get("policy") == "verify-purity/v1"
            and execution.get("integrity") == "pure"
        )
        if execution.get("assertion_result") != "passed" or not valid_integrity:
            fail(f"required task {task_id} lacks supported passing Walden execution integrity")
        steps = task.get("steps")
        if not isinstance(steps, list) or not steps or any(
            step.get("actual_exit") != step.get("expected_exit") or step.get("actual_exit") != 0
            for step in steps
        ):
            fail(f"required task {task_id} has a failed or unrun verification step")
        row = re.compile(rf"^\|\s*{re.escape(task_id)}\s*\|.*\|\s*PASS\s*\|\s*$", re.MULTILINE)
        if not row.search(outcome_section):
            fail(f"verification report does not record task {task_id} as passed")

    for task_id in ("4.7",):
        row = re.compile(rf"^\|\s*{re.escape(task_id)}\s*\|.*\|\s*PASS\s*\|\s*$", re.MULTILINE)
        if not row.search(outcome_section):
            fail(f"verification report does not record final audit task {task_id} as passed")

    log = git_output("log", "--reverse", "--format=%H%x09%s", f"{records['baseline_commit']}..HEAD")
    commits: list[tuple[str, str]] = []
    for line in log.splitlines():
        sha, separator, subject = line.partition("\t")
        if separator:
            commits.append((sha, subject))
    required_subjects = (
        "spec: define KubeFacet identity migration",
        "refactor: rename Kubernetes API and runtime identity",
        "build: rename KubeFacet packaging and distribution",
        "docs: complete KubeFacet migration",
        "test: certify KubeFacet package lifecycle",
    )
    positions: list[int] = []
    for subject in required_subjects:
        try:
            positions.append(next(index for index, (_, value) in enumerate(commits) if value == subject))
        except StopIteration:
            fail(f"required coherent migration commit is missing: {subject}")
    if positions != sorted(positions):
        fail("migration commits do not preserve specification-first implementation order")

    expected_paths = {
        required_subjects[0]: {
            ".walden/specs/project-identity-rename/requirements.md",
            ".walden/specs/project-identity-rename/design.md",
            ".walden/specs/project-identity-rename/tasks.md",
            ".walden/specs/project-identity-rename/api-schema-baseline.json",
        },
        required_subjects[1]: {"api/v1alpha1/facet_types.go", "internal/managerapp/application.go", "go.mod"},
        required_subjects[2]: {
            "charts/kubefacet/Chart.yaml",
            "hack/toolchain.mk",
            "examples/builtin-resource/facet.yaml",
        },
        required_subjects[3]: {
            "README.md",
            ".walden/current-identity.md",
            f"docs/migration-from-{TOKEN}.md",
        },
        required_subjects[4]: {
            "hack/test-project-identity-package.sh",
            "hack/package-cluster-smoke.sh",
            "hack/verify_project_identity.py",
        },
    }
    for subject, required in expected_paths.items():
        sha = commits[next(index for index, (_, value) in enumerate(commits) if value == subject)][0]
        changed = set(git_output("diff-tree", "--no-commit-id", "--name-only", "-r", sha).splitlines())
        missing = required - changed
        if missing:
            fail(f"commit {subject!r} has an incoherent scope; missing paths: {sorted(missing)}")
        normalized_report = " ".join(report.split())
        if sha not in report or subject not in normalized_report:
            fail(f"verification report does not identify commit {sha[:12]} ({subject})")

    if "This selected-feature verdict does not certify the preserved legacy portfolio" not in report:
        fail("verification report does not bound Walden readiness to the selected feature")
    print(
        "PROJECT_IDENTITY=delivery STATUS=passed "
        f"TASKS={len(expected_task_ids)} COMMITS={len(required_subjects)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        nargs="?",
        choices=("all", "api", "audit", "audit-acceptance", "builds", "delivery", "docs", "environment", "history", "local", "observability", "package", "release", "runtime"),
        default="audit",
    )
    args = parser.parse_args()
    try:
        if args.mode == "all":
            run_all()
        elif args.mode == "delivery":
            run_delivery()
        elif args.mode == "history":
            run_history()
        elif args.mode == "docs":
            run_docs()
        elif args.mode == "audit-acceptance":
            run_audit_acceptance()
        elif args.mode == "audit":
            run_audit()
        elif args.mode == "api":
            run_api()
        elif args.mode == "builds":
            run_builds()
        elif args.mode == "runtime":
            run_runtime()
        elif args.mode == "observability":
            run_observability()
        elif args.mode == "package":
            run_package()
        elif args.mode == "release":
            run_release()
        elif args.mode == "environment":
            run_environment()
        elif args.mode == "local":
            run_local()
    except VerificationError as exc:
        print(f"project identity verification failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
