---
walden_schema_version: v1alpha1
status: approved
approved_at: 2026-09-26T12:03:32Z
last_modified: 2026-09-26T22:07:37Z
approved_fingerprint: sha256:a33b0f23bbdc1596f46ab185b22593430af89fbb51a6b0012ff0480f510ece84
source_design_approved_at: 2026-09-26T11:43:39Z
source_design_fingerprint: sha256:920f58501881f319cd87010fcb2e02028ef4e00e513dc4c2bc833cfa4e88c31d
---

# KubeFacet Identity Migration Implementation Tasks

Execute the numbered tasks in order after this plan is explicitly approved.
The maintainer has already requested full implementation and local reviewable
commits; task-plan approval unlocks that existing execution scope. Do not ask
for a second implementation authorization. This task plan creates no release,
public push, hosted repository rename, remote update, or historical retirement.

Every leaf owns its new assertions and records completion through the Walden
CLI. Generator/sync commands are implementation actions; proof commands are
read-only and may write only isolated build, cache, registry, cluster, or
verification outputs outside the repository. Use writable kubefacet cache/tmp
roots and supported toolchain inputs. Invoke container/listener-dependent
proofs with the runtime access needed for genuine Podman/envtest execution.
Do not complete a leaf through a fallback that skips its required assertion.

The verification interfaces below are implementation deliverables, not tools
already present. Their pass markers are emitted only after actual assertions:
history checks exact preserved bytes and baseline provenance; api compares
scheme/generated schema; runtime checks admission/defaults/ownership; builds
compiles all three renamed commands into a temporary directory; observability
checks all nine collector contracts; package checks renders/metadata/copies/
hashes; release checks canonical destinations/source note/workflow handoff;
environment checks project settings and state/cache paths; local checks
example/catalog/selector/probe coupling; docs checks current terminology,
breaking procedure, and post-merge actions; audit scans real text and paths
including hidden/Walden files and enumerates classified matches; acceptance
runs negative injections on isolated copies. The all mode combines the full
identity contract, not the unrelated aggregate test executions. The delivery
mode checks actual report completeness, honest outcomes, and commit order.
No stage mode may be described as a passing final residue audit.

Keep the existing behavioral test cases and add the named integration cases
under TestModuleIntegration. A named PASS is required so an unmatched Go
selector cannot produce evidence. Long proof budgets accommodate the current
full matrices/real clusters/registry transactions; they do not allow silent
skips. Run genuine cluster workflows sequentially to avoid shared runtime or
port conflicts. Final aggregate proofs follow all implementation/current-doc
edits; only metadata/report/evidence updates should remain afterwards.

The preferred commit groups are specification; API/module/runtime; package/
distribution/local/examples; current documentation/contracts. One closely
related final evidence commit is acceptable. Intermediate focused evidence is
scoped; complete migration claims require every aggregate checkpoint below.

- [x] 1. Preserve the reviewed contract and establish verification baselines

  - [x] 1.1 Record the reviewed specification and original generated API baseline
    - Scope: Before any implementation edit, capture both complete baseline CRDs as self-contained migration data in api-schema-baseline.json. Its baseline_commit matches the historical inventory; resources facet and access-policy each contain source_path, sha256, and content_b64. Preserve all original fields and constraints. Commit only the complete reviewed specification, inventory, and schema baseline as spec: define KubeFacet identity migration. The baseline is historical migration data, not new execution evidence.
    - Requirements: `R12.AC1`, `R12.AC4`, `R2.AC6`, `NFR2`, `NFR3`, `NFR5`, `C2`, `C6`, `C8`, `C9`
    - Design: Architecture / Generated Schema And Semantic Baselines; Architecture / Current Contracts, History, And Migration Documentation; Verification Plan
    - Verification:
      - command: ["python3", "-c", "from pathlib import Path; import base64,hashlib,json,re,subprocess; root=Path('.walden/specs/project-identity-rename'); docs=[root/name for name in ['requirements.md','design.md','tasks.md']]; assert all(re.search(r'^status: approved$',p.read_text(),re.M) and re.search(r'^approved_fingerprint: sha256:[0-9a-f]{64}$',p.read_text(),re.M) for p in docs), 'review chain not approved'; baseline=json.loads((root/'api-schema-baseline.json').read_text()); records=json.loads((root/'historical-identity-records.json').read_text()); assert baseline['baseline_commit']==records['baseline_commit']; assert set(baseline['resources'])=={'facet','access-policy'}; snapshots=[(r,base64.b64decode(r['content_b64'],validate=True)) for r in baseline['resources'].values()]; assert all(hashlib.sha256(raw).hexdigest()==r['sha256'] and subprocess.check_output(['git','show',baseline['baseline_commit']+':'+r['source_path']])==raw for r,raw in snapshots), 'baseline does not match immutable source'; assert any(s=='spec: define KubeFacet identity migration' for s in subprocess.check_output(['git','log','--format=%s',baseline['baseline_commit']+'..HEAD'],text=True).splitlines()), 'specification commit missing'; print('PROJECT_IDENTITY=specification STATUS=passed BASELINE_RESOURCES=2')"]
        expect_output: "PROJECT_IDENTITY=specification STATUS=passed BASELINE_RESOURCES=2"
        timeout: 10m
        covers: ["R12.AC1", "R12.AC4", "R2.AC6", "NFR2", "NFR3", "NFR5", "C2", "C6", "C8", "C9"]

  - [x] 1.2 Implement read-only historical, schema, and identity verification interfaces
    - Scope: Implement hack/verify-project-identity.sh and its narrowly scoped helpers. The history mode validates all 98 preserved records and baseline provenance; schema/API modes parse the archived and newly generated CRDs using the existing Go/YAML toolchain. Implement exact historical and occurrence-level exception handling, hidden/Walden/path scanning, and positive identity assertions as described in the approved design. Build audit-acceptance scenarios on isolated copies, including old imports, group/Kinds, settings, metrics, selectors, mixed case, path-only residue, new Walden contracts, and changes to an allowed mixed document. No blanket directory/document exemptions or automatic hash acceptance. At this stage history and isolated audit acceptance can pass while the real repository still requires migration; the default/final gate must continue rejecting actual operational residue.
    - Requirements: `R11.AC1`, `R11.AC4`, `R11.AC5`, `R12.AC2`, `NFR2`, `NFR3`, `NFR5`, `C3`, `C9`
    - Design: Architecture / Durable Identity Verification; Architecture / Generated Schema And Semantic Baselines; Failure Modes And Tradeoffs
    - Verification:
      - command: ["./hack/verify-project-identity.sh", "history"]
        expect_output: "PROJECT_IDENTITY=history STATUS=passed"
        timeout: 10m
        covers: ["R11.AC1", "NFR3", "C9"]
      - command: ["./hack/verify-project-identity.sh", "audit-acceptance"]
        expect_output: "PROJECT_IDENTITY=audit-acceptance STATUS=passed"
        timeout: 10m
        covers: ["R11.AC4", "R11.AC5", "R12.AC2", "NFR2", "NFR5", "C3"]

- [x] 2. Migrate the Go API, runtime identities, and observability

  - [x] 2.1 Rename the Go module, public API, consumers, paths, and generated API artifacts
    - Scope: Rename the module and all internal imports, main/supporting command directories, API source/test files, public and equivalent nested/resource helper identifiers, and all typed consumers/test fixtures. Change GroupVersion, scheme registration, markers, plurals, and singulars; keep the policy singleton. Update Makefile and Dockerfile command/build/entrypoint paths with the directory moves; OCI/package branding follows in task 3.1. Preserve JSON tags, fields, constraints, and functional assertions. Regenerate deepcopy and CRDs with make generate and make manifests, remove the obsolete generated CRDs, and compare the semantic schema baseline. Add a ProjectIdentityAPI case within TestModuleIntegration that crosses API/scheme and real policy/admission or resource-store boundaries and asserts exact new identities and absence of aliases. A full repository gate is deferred until packaging/docs also migrate.
    - Requirements: `R2.AC1`, `R2.AC2`, `R2.AC3`, `R2.AC4`, `R2.AC6`, `R2.AC7`, `R3.AC1`, `R3.AC2`, `R3.AC3`, `R3.AC4`, `R7.AC7`, `R12.AC2`, `NFR1`, `NFR2`, `C1`, `C2`, `C3`, `C4`
    - Design: Architecture / Authoritative Identity Mapping; Architecture / API, Admission, And Runtime Coupling; Architecture / Generated Schema And Semantic Baselines
    - Verification:
      - command: ["./hack/verify-project-identity.sh", "api"]
        expect_output: "PROJECT_IDENTITY=api STATUS=passed"
        timeout: 10m
        covers: ["R2.AC1", "R2.AC2", "R2.AC4", "R2.AC6", "R2.AC7", "R3.AC1", "R3.AC4", "R7.AC7", "NFR1", "NFR2", "C1", "C2", "C3", "C4"]
      - command: ["go", "test", "-v", "-count=1", "-run", "^TestModuleIntegration$/^ProjectIdentityAPI$", "./test/integration/..."]
        expect_output: "--- PASS: TestModuleIntegration/ProjectIdentityAPI"
        timeout: 10m
        covers: ["R2.AC1", "R2.AC2", "R2.AC3", "R2.AC4", "R2.AC7", "R12.AC2", "NFR1"]
      - command: ["./hack/verify-project-identity.sh", "builds"]
        expect_output: "PROJECT_IDENTITY=builds STATUS=passed"
        timeout: 10m
        covers: ["R3.AC1", "R3.AC2", "R3.AC3", "R3.AC4", "NFR2"]

  - [x] 2.2 Rename admission and runtime identities without changing decisions or lifecycle rules
    - Scope: Coordinate webhook endpoints/names/rules, manager and certificate defaults/SANs, Deployment/Service/ServiceAccount/webhook names, project labels/annotations, controller/leader-election/Event/logger/field-manager names, storage-version helper/flag names, CLI output, runtime settings, and purge confirmation. Rename the uninstall helper path. Update each matching lifecycle/readiness/cleanup selector and behavioral expectation. Add ProjectIdentityRuntime to TestModuleIntegration, composing real manager configuration, webhook registration, and ownership/purge contracts. Update the active admission boundary check to enforce new API identities while retaining its original structural assertions.
    - Requirements: `R1.AC3`, `R1.AC4`, `R1.AC6`, `R2.AC5`, `R2.AC7`, `R4.AC1`, `R4.AC2`, `R4.AC3`, `R4.AC4`, `R4.AC5`, `R5.AC1`, `R5.AC2`, `R12.AC2`, `NFR1`, `NFR4`, `C1`, `C2`
    - Design: Architecture / API, Admission, And Runtime Coupling; Architecture / Environment, State, And Telemetry; Failure Modes And Tradeoffs
    - Verification:
      - command: ["./hack/verify-project-identity.sh", "runtime"]
        expect_output: "PROJECT_IDENTITY=runtime STATUS=passed"
        timeout: 10m
        covers: ["R2.AC5", "R2.AC7", "R4.AC1", "R4.AC2", "R4.AC3", "R4.AC4", "R4.AC5", "R5.AC1", "R5.AC2", "C1", "C2"]
      - command: ["go", "test", "-v", "-count=1", "-run", "^TestModuleIntegration$/^ProjectIdentityRuntime$", "./test/integration/..."]
        expect_output: "--- PASS: TestModuleIntegration/ProjectIdentityRuntime"
        timeout: 10m
        covers: ["R1.AC3", "R1.AC4", "R1.AC6", "R4.AC1", "R4.AC2", "R4.AC3", "R4.AC4", "R4.AC5", "R12.AC2", "NFR1", "NFR4"]
      - command: ["./hack/verify-admission-boundaries.sh"]
        expect_output: "Admission boundary verification passed"
        timeout: 10m
        covers: ["R1.AC3", "R2.AC5", "NFR1"]

  - [x] 2.3 Rename all telemetry identifiers while retaining their observation contracts
    - Scope: Rename the nine metric families, Help text, trace instrumentation/spans/attributes, and project correlation/log identifiers; update registration checks, integration expectations, and relevant probes. Preserve collector types, buckets, label sets/vocabularies, increments, Event rules, and confidentiality. Add ProjectIdentityObservability to TestModuleIntegration using real observation/registration and status or authorization collaborators; execute the existing observability cases alongside it. Commit the related verification helpers, module/API/runtime/telemetry changes, generated API artifacts, and scoped evidence as refactor: rename Kubernetes API and runtime identity.
    - Requirements: `R1.AC5`, `R6.AC1`, `R6.AC2`, `R6.AC3`, `R4.AC3`, `R4.AC5`, `R12.AC2`, `R12.AC4`, `NFR1`, `NFR2`, `NFR5`
    - Design: Architecture / Environment, State, And Telemetry; Architecture / API, Admission, And Runtime Coupling; Verification Plan
    - Verification:
      - command: ["./hack/verify-project-identity.sh", "observability"]
        expect_output: "PROJECT_IDENTITY=observability STATUS=passed"
        timeout: 10m
        covers: ["R6.AC1", "R6.AC2", "R6.AC3", "R4.AC3", "R4.AC5", "NFR1", "NFR2"]
      - command: ["go", "test", "-v", "-count=1", "-run", "^TestModuleIntegration$/^(ProjectIdentityObservability|observability.*)$", "./test/integration/..."]
        expect_output: "--- PASS: TestModuleIntegration/ProjectIdentityObservability"
        timeout: 10m
        covers: ["R1.AC5", "R6.AC1", "R6.AC2", "R6.AC3", "R12.AC2", "NFR1"]
      - command: ["./hack/verify-observability-boundaries.sh"]
        expect_output: "Observability boundary verification passed"
        timeout: 10m
        covers: ["R1.AC5", "R6.AC1", "R6.AC2", "R6.AC3", "NFR1"]

- [x] 3. Migrate packaging, distribution, local workflows, and examples

  - [x] 3.1 Rename the Helm package, container distribution identity, and generated metadata
    - Scope: Move charts/kubefacet; update all helper/include namespaces, metadata, names/selectors, schemas/values, default image/release/namespace, CRD filenames/copies, config profiles, Dockerfile executable and OCI metadata, and package test expectations. Set description/keywords and version/appVersion 0.2.0 while retaining the Kubernetes range/matrix and container/RBAC/TLS/lifecycle semantics. Extend package-sync-crds to derive both new-domain checksum annotations and run make package-sync-crds after canonical generation. Add any missing positive chart assertions to the package identity mode. Prepare the disposable genuine-package-matrix wrapper described below; it must invoke the existing smoke/compatibility procedure on owned clusters without adding a new product installation path.
    - Requirements: `R1.AC6`, `R4.AC1`, `R4.AC2`, `R4.AC4`, `R7.AC1`, `R7.AC2`, `R7.AC3`, `R7.AC4`, `R7.AC5`, `R7.AC6`, `R7.AC7`, `R7.AC8`, `R8.AC1`, `R8.AC2`, `R8.AC3`, `R12.AC2`, `NFR1`, `NFR2`, `C1`, `C3`, `C4`, `C5`
    - Design: Architecture / Packaging, Generation, And Distribution; Architecture / API, Admission, And Runtime Coupling; Verification Plan
    - Verification:
      - command: ["./hack/verify-generated.sh"]
        expect_output: "generated artifacts are current"
        timeout: 10m
        covers: ["R7.AC7", "NFR2", "C3"]
      - command: ["./hack/verify-project-identity.sh", "package"]
        expect_output: "PROJECT_IDENTITY=package STATUS=passed"
        timeout: 10m
        covers: ["R7.AC1", "R7.AC2", "R7.AC3", "R7.AC4", "R7.AC5", "R7.AC6", "R7.AC7", "R7.AC8", "R4.AC1", "R4.AC2", "R4.AC4", "R8.AC1", "R8.AC2", "R8.AC3", "NFR1", "NFR2", "C1", "C3", "C4"]
      - command: ["make", "test-package-compatibility"]
        expect_output: "PACKAGE_COMPATIBILITY=complete STATUS=passed"
        timeout: 10m
        covers: ["R1.AC6", "R7.AC4", "R12.AC2", "NFR1", "C4"]

  - [x] 3.2 Rename release tooling and workflow handoff while preserving publication safety
    - Scope: Update canonical repository/image/chart/archive identities, source/OCI metadata, locks/temp roots, workflow group/output paths, project-owned endpoint/fixture/SHA-handoff settings, and synthetic 0.2.x candidate versions. Preserve protected-tag lineage, exact gated SHA, limited permissions, immutable artifacts, local-endpoint restrictions, retry/recovery/conflict behavior, and anonymous consumer checks. Add truthful docs/releases/v0.2.0.md source metadata required by existing preflight; do not tag, push, publish, rename hosting, or touch historical packages. Run focused source-policy/workflow proofs here; all candidate/transaction/docs scenarios run at the final distribution checkpoint after current docs are finished.
    - Requirements: `R8.AC1`, `R8.AC2`, `R8.AC3`, `R8.AC4`, `R8.AC5`, `R5.AC1`, `R5.AC2`, `R5.AC3`, `R12.AC2`, `NFR3`, `NFR4`, `C1`, `C4`, `C7`
    - Design: Architecture / Packaging, Generation, And Distribution; Architecture / Environment, State, And Telemetry; Failure Modes And Tradeoffs
    - Verification:
      - command: ["./hack/verify-project-identity.sh", "release"]
        expect_output: "PROJECT_IDENTITY=release STATUS=passed"
        timeout: 10m
        covers: ["R8.AC1", "R8.AC2", "R8.AC3", "R5.AC1", "R5.AC2", "R5.AC3", "C1", "C7"]
      - command: ["make", "test-release-distribution", "SCENARIO=policy"]
        expect_output: "RELEASE_DISTRIBUTION=policy STATUS=passed"
        timeout: 20m
        covers: ["R8.AC1", "R8.AC4", "R8.AC5", "R12.AC2", "NFR3", "NFR4", "C4", "C7"]
      - command: ["make", "test-release-distribution", "SCENARIO=workflows"]
        expect_output: "RELEASE_DISTRIBUTION=workflows STATUS=passed"
        timeout: 15m
        covers: ["R8.AC4", "R8.AC5", "NFR4", "C7"]

  - [x] 3.3 Rename project settings, local/E2E identities, examples, and all coupled harness consumers
    - Scope: Migrate remaining project-owned environment producers/consumers, including dynamic per-version names, unprefixed project settings, and fault injection; retain standard upstream variables and neutral Make inputs. Rename all local/E2E/default namespace/context/release/image/state/cache/temp/diagnostic/fixture/sentinel identities. Rename the seven example resource manifests to facet.yaml and coordinate custom fixture domains, object names, namespaces, selectors, and references while retaining workloads and example semantics. Update toolchain, probes, ownership/resume/cleanup checks, acceptance fixtures, and E2E certification contracts. Exercise deterministic acceptance here, with genuine tests reserved for the final checkpoint. Commit these packaging/distribution/local/example changes and scoped evidence as build: rename KubeFacet packaging and distribution.
    - Requirements: `R5.AC1`, `R5.AC2`, `R5.AC3`, `R9.AC1`, `R9.AC2`, `R9.AC3`, `R9.AC4`, `R9.AC5`, `R4.AC2`, `R4.AC4`, `R4.AC5`, `R12.AC2`, `R12.AC4`, `NFR1`, `NFR4`, `NFR5`, `C4`, `C5`
    - Design: Architecture / Environment, State, And Telemetry; Architecture / Local Development And Examples; Architecture / Packaging, Generation, And Distribution
    - Verification:
      - command: ["./hack/verify-project-identity.sh", "environment"]
        expect_output: "PROJECT_IDENTITY=environment STATUS=passed"
        timeout: 10m
        covers: ["R5.AC1", "R5.AC2", "R5.AC3", "NFR4", "C4"]
      - command: ["./hack/verify-project-identity.sh", "local"]
        expect_output: "PROJECT_IDENTITY=local STATUS=passed"
        timeout: 10m
        covers: ["R9.AC1", "R9.AC2", "R9.AC3", "R9.AC4", "R4.AC2", "R4.AC4", "R4.AC5", "NFR1", "C5"]
      - command: ["./hack/local-environment-acceptance.sh", "complete"]
        expect_output: "LOCAL_ENVIRONMENT_ACCEPTANCE=complete STATUS=passed"
        timeout: 20m
        covers: ["R9.AC1", "R9.AC2", "R9.AC3", "R12.AC2", "NFR4", "C5"]
      - command: ["./hack/e2e-harness-acceptance.sh"]
        expect_output: "E2E_HARNESS_ACCEPTANCE=complete STATUS=passed"
        timeout: 20m
        covers: ["R9.AC2", "R9.AC3", "R4.AC4", "R12.AC2", "NFR4", "C5"]

- [ ] 4. Complete current contracts and certify the final migration

  - [x] 4.1 Complete current documentation, identity supersession, and the real repository residue gate
    - Scope: Update README, CONTRIBUTING, API/install/config/security/operations/troubleshooting/development/example/Helm documentation, SPECIFICATIONS, and constitution. Retain positioning, semantic guidance, optional contributor Walden usage, and historical feature IDs with explicit explanations. Create .walden/current-identity.md and docs/migration-from-kubeseer.md; point old lifecycle removal to immutable v0.1.6 documentation/tooling, document unsupported in-place upgrade/no conversion, and list all manual post-merge actions. Treat historical release-audit observations separately from current instructions. Review and record exact occurrence/path exceptions for migration explanations and historical links; retain all historical bytes. Integrate the audit into make verify/CI and require it to pass on the real repository. Prepare the durable verification report structure before aggregate proofs so later observations do not introduce new operational code. Commit documentation/current-contract changes as docs: complete KubeFacet migration.
    - Requirements: `R10.AC1`, `R10.AC2`, `R10.AC3`, `R10.AC4`, `R10.AC5`, `R10.AC6`, `R11.AC1`, `R11.AC2`, `R11.AC3`, `R11.AC4`, `R11.AC5`, `R11.AC6`, `R12.AC2`, `R12.AC4`, `NFR3`, `NFR5`, `C4`, `C6`, `C7`, `C9`
    - Design: Architecture / Current Contracts, History, And Migration Documentation; Architecture / Durable Identity Verification; Verification Plan
    - Verification:
      - command: ["./hack/verify-project-identity.sh", "docs"]
        expect_output: "PROJECT_IDENTITY=docs STATUS=passed"
        timeout: 10m
        covers: ["R10.AC1", "R10.AC2", "R10.AC3", "R10.AC4", "R10.AC5", "R10.AC6", "R11.AC2", "R11.AC3", "NFR3", "NFR5", "C4", "C7", "C9"]
      - command: ["./hack/verify-project-identity.sh", "history"]
        expect_output: "PROJECT_IDENTITY=history STATUS=passed"
        timeout: 10m
        covers: ["R11.AC1", "NFR3", "C9"]
      - command: ["./hack/verify-project-identity.sh", "audit"]
        expect_output: "PROJECT_IDENTITY=audit STATUS=passed"
        timeout: 10m
        covers: ["R11.AC3", "R11.AC4", "R11.AC5", "R11.AC6", "R12.AC2", "NFR3", "NFR5"]
      - command: ["./hack/verify-project-identity.sh", "audit-acceptance"]
        expect_output: "PROJECT_IDENTITY=audit-acceptance STATUS=passed"
        timeout: 10m
        covers: ["R11.AC4", "R11.AC5", "R11.AC6", "R12.AC2", "NFR5"]

  - [x] 4.2 Pass the final canonical repository, integration, API, and render compatibility checks
    - Scope: Run the canonical source/generated/boundary/package/local gates and default real module suite against the finished implementation. Run the complete supported envtest matrix, including generated API/schema, discovery/selection, reconciliation/authorization/status Events, and admission. Run both-version/both-TLS-mode package render checks. Preserve original behavioral assertions, use noncached execution, run renamed manager/helper builds into temporary roots, and assert read-only module consistency. This is the aggregate semantic checkpoint; focused earlier identity tests do not replace it.
    - Requirements: `R1.AC1`, `R1.AC2`, `R1.AC3`, `R1.AC4`, `R1.AC5`, `R1.AC6`, `R2.AC1`, `R2.AC2`, `R2.AC3`, `R2.AC5`, `R2.AC6`, `R2.AC7`, `R3.AC1`, `R3.AC2`, `R3.AC3`, `R4.AC1`, `R4.AC2`, `R4.AC3`, `R4.AC4`, `R6.AC1`, `R6.AC2`, `R6.AC3`, `R7.AC4`, `R7.AC7`, `R7.AC8`, `R11.AC6`, `R12.AC2`, `R12.AC3`, `NFR1`, `NFR2`, `C2`, `C3`, `C4`
    - Design: Verification Plan; Architecture / Generated Schema And Semantic Baselines; Architecture / API, Admission, And Runtime Coupling
    - Verification:
      - command: ["make", "verify"]
        expect_output: "PROJECT_IDENTITY=audit STATUS=passed"
        timeout: 30m
        covers: ["R2.AC6", "R4.AC1", "R4.AC2", "R4.AC3", "R4.AC4", "R7.AC7", "R7.AC8", "R11.AC6", "R12.AC3", "NFR2", "C3"]
      - command: ["make", "test", "GO_TEST_FLAGS=-count=1"]
        expect_output: "TEST_LAYER=module-integration STATUS=passed"
        timeout: 20m
        covers: ["R1.AC1", "R1.AC2", "R1.AC3", "R1.AC4", "R1.AC5", "R1.AC6", "R6.AC1", "R6.AC2", "R6.AC3", "R12.AC2", "R12.AC3", "NFR1", "NFR2", "C2"]
      - command: ["make", "test-compatibility", "GO_TEST_FLAGS=-count=1", "KUBERNETES_COMPATIBILITY_VERSIONS=1.35.6 1.36.2"]
        expect_output: "API compatibility matrix passed"
        timeout: 45m
        covers: ["R1.AC1", "R1.AC3", "R1.AC4", "R2.AC1", "R2.AC2", "R2.AC3", "R2.AC5", "R2.AC6", "R2.AC7", "R7.AC4", "R12.AC3", "NFR1", "NFR2", "C4"]
      - command: ["make", "test-package-compatibility"]
        expect_output: "PACKAGE_COMPATIBILITY=complete STATUS=passed"
        timeout: 10m
        covers: ["R1.AC6", "R7.AC4", "R12.AC3", "NFR1", "C4"]
      - command: ["./hack/verify-project-identity.sh", "builds"]
        expect_output: "PROJECT_IDENTITY=builds STATUS=passed"
        timeout: 15m
        covers: ["R3.AC1", "R3.AC2", "R3.AC3", "NFR2"]
      - command: ["go", "mod", "tidy", "-diff"]
        timeout: 10m
        covers: ["R3.AC1", "NFR2"]

  - [x] 4.3 Prove genuine local development, examples, diagnostics, and owned-node resume
    - Scope: With working rootless Podman, execute the genuine persistent local workflow using dedicated new-identity state/cache roots and the seven current examples. Require the genuine EndpointSlice marker, sanitized diagnostics, retained source/worktree state, and bounded owned cleanup. Execute genuine exited-node resume on its run-unique owned fixture, retaining container/workload identity and the existing ownership/read-only rejection behavior. A deterministic/fake-tool fallback may still supplement the suite but cannot complete this task.
    - Requirements: `R1.AC6`, `R4.AC1`, `R4.AC2`, `R4.AC4`, `R4.AC5`, `R5.AC3`, `R9.AC1`, `R9.AC2`, `R9.AC3`, `R9.AC4`, `R9.AC5`, `R12.AC3`, `NFR1`, `NFR4`, `C5`
    - Design: Architecture / Local Development And Examples; Verification Plan; Failure Modes And Tradeoffs
    - Verification:
      - command: ["make", "local-check"]
        expect_output: "LOCAL_ENVIRONMENT=check STATUS=passed"
        timeout: 10m
        covers: ["R9.AC2", "C5"]
      - command: ["make", "test-local-environment"]
        expect_output: "LOCAL_ENDPOINTSLICE_ACCEPTANCE=genuine STATUS=passed"
        timeout: 60m
        covers: ["R1.AC6", "R4.AC1", "R4.AC2", "R4.AC4", "R4.AC5", "R5.AC3", "R9.AC1", "R9.AC2", "R9.AC3", "R9.AC4", "R9.AC5", "R12.AC3", "NFR1", "NFR4", "C5"]
      - command: ["make", "test-local-cluster-resume"]
        expect_output: "LOCAL_CLUSTER_RESUME_ACCEPTANCE=genuine STATUS=passed"
        timeout: 60m
        covers: ["R1.AC6", "R9.AC1", "R9.AC2", "R9.AC3", "R12.AC3", "NFR4", "C5"]

  - [x] 4.4 Certify genuine package lifecycle compatibility on the supported Podman matrix
    - Scope: Use hack/test-project-identity-package.sh as an owned disposable-cluster wrapper around the existing package compatibility/smoke procedure. Create run-unique kind-on-Podman clusters for 1.35.6 and 1.36.2 using the declared images, build/load the current manager once as appropriate, prepare both existing certificate modes (including external Secret rotation fixtures), and pass only explicit absolute kubeconfigs/contexts and new-prefix package settings. Invoke make test-package-compatibility with genuine cluster execution enabled. Require all four version/mode smoke profile pass records and preservation of unrelated resources, author RBAC separation, policy/bootstrap/admission, upgrade/rollback/uninstall/confirmed-purge, owned cleanup, and unchanged source snapshots. Never attach to ambient or historical installations.
    - Requirements: `R1.AC3`, `R1.AC6`, `R2.AC1`, `R2.AC2`, `R2.AC3`, `R2.AC5`, `R4.AC1`, `R4.AC2`, `R4.AC4`, `R7.AC4`, `R7.AC5`, `R7.AC6`, `R9.AC2`, `R9.AC3`, `R12.AC2`, `R12.AC3`, `NFR1`, `NFR2`, `NFR4`, `C4`, `C5`
    - Design: Architecture / Packaging, Generation, And Distribution; Architecture / Local Development And Examples; Verification Plan
    - Verification:
      - command: ["./hack/test-project-identity-package.sh"]
        expect_output: "PROJECT_IDENTITY=package-cluster STATUS=passed PROFILES=4"
        timeout: 90m
        covers: ["R1.AC3", "R1.AC6", "R2.AC1", "R2.AC2", "R2.AC3", "R2.AC5", "R4.AC1", "R4.AC2", "R4.AC4", "R7.AC4", "R7.AC5", "R7.AC6", "R9.AC2", "R9.AC3", "R12.AC2", "R12.AC3", "NFR1", "NFR2", "NFR4", "C4", "C5"]

  - [x] 4.5 Run every E2E certification scenario on both supported Kubernetes versions
    - Scope: Run the canonical E2E harness acceptance and all 15 existing product scenarios for each supported version. Preserve all 20 minimum-scenario mappings, public product boundaries, real authorization/admission/status/metric assertions, ownership, lifecycle, explicit kubeconfig/context, diagnostics, and cleanup. Use the existing Podman harness and pinned version/image inputs; require both completed named suites and the version-specific certification output. No skipped scenario or external-cluster fallback is acceptable.
    - Requirements: `R1.AC1`, `R1.AC2`, `R1.AC3`, `R1.AC4`, `R1.AC5`, `R1.AC6`, `R2.AC1`, `R2.AC2`, `R2.AC3`, `R2.AC5`, `R4.AC1`, `R4.AC2`, `R4.AC3`, `R4.AC4`, `R4.AC5`, `R5.AC1`, `R5.AC2`, `R5.AC3`, `R6.AC1`, `R6.AC2`, `R6.AC3`, `R7.AC4`, `R9.AC1`, `R9.AC2`, `R9.AC3`, `R9.AC5`, `R12.AC2`, `R12.AC3`, `NFR1`, `NFR2`, `NFR4`, `C4`, `C5`
    - Design: Verification Plan; Architecture / API, Admission, And Runtime Coupling; Architecture / Local Development And Examples
    - Verification:
      - command: ["./hack/e2e-harness-acceptance.sh"]
        expect_output: "E2E_HARNESS_ACCEPTANCE=complete STATUS=passed"
        timeout: 20m
        covers: ["R9.AC2", "R9.AC3", "R12.AC2", "NFR4", "C5"]
      - command: ["make", "e2e", "KUBERNETES_VERSION=1.35.6", "GO_TEST_FLAGS=-count=1"]
        expect_output: "--- PASS: TestEndToEnd"
        timeout: 60m
        covers: ["R1.AC1", "R1.AC2", "R1.AC3", "R1.AC4", "R1.AC5", "R1.AC6", "R2.AC1", "R2.AC2", "R2.AC3", "R2.AC5", "R4.AC1", "R4.AC2", "R4.AC3", "R4.AC4", "R4.AC5", "R5.AC1", "R5.AC2", "R5.AC3", "R6.AC1", "R6.AC2", "R6.AC3", "R7.AC4", "R9.AC1", "R9.AC2", "R9.AC3", "R9.AC5", "R12.AC2", "R12.AC3", "NFR1", "NFR2", "NFR4", "C4", "C5"]
      - command: ["make", "e2e", "KUBERNETES_VERSION=1.36.2", "GO_TEST_FLAGS=-count=1"]
        expect_output: "--- PASS: TestEndToEnd"
        timeout: 60m
        covers: ["R1.AC1", "R1.AC2", "R1.AC3", "R1.AC4", "R1.AC5", "R1.AC6", "R2.AC1", "R2.AC2", "R2.AC3", "R2.AC5", "R4.AC1", "R4.AC2", "R4.AC3", "R4.AC4", "R4.AC5", "R5.AC1", "R5.AC2", "R5.AC3", "R6.AC1", "R6.AC2", "R6.AC3", "R7.AC4", "R9.AC1", "R9.AC2", "R9.AC3", "R9.AC5", "R12.AC2", "R12.AC3", "NFR1", "NFR2", "NFR4", "C4", "C5"]

  - [x] 4.6 Pass every release-distribution scenario against disposable local endpoints
    - Scope: Run all five canonical scenarios after current release/install/contributor documentation is complete. Require candidate build/staging, actual local Podman image and Helm OCI chart transactions, anonymous pull/render, immutable conflicts, partial-publication recovery/retry behavior, tag/source policies, workflows, and consumer documentation to pass. Keep the pre-existing local-endpoint restrictions and ownership cleanup; do not run the publisher against GHCR/GitHub production. Record the new 0.2.x fixture identities and all five scenario pass records.
    - Requirements: `R8.AC1`, `R8.AC2`, `R8.AC3`, `R8.AC4`, `R8.AC5`, `R5.AC1`, `R5.AC2`, `R5.AC3`, `R7.AC1`, `R7.AC5`, `R7.AC6`, `R10.AC1`, `R12.AC2`, `R12.AC3`, `NFR2`, `NFR3`, `NFR4`, `C1`, `C4`, `C7`
    - Design: Architecture / Packaging, Generation, And Distribution; Verification Plan; Failure Modes And Tradeoffs
    - Verification:
      - command: ["bash", "-c", "set -eu; proof_dir=$(mktemp -d \"${TMPDIR:-/tmp}/kubefacet-release-proof.XXXXXX\"); trap 'rm -rf -- \"$proof_dir\"' EXIT; if make test-release-distribution SCENARIO=all >\"$proof_dir/output\" 2>&1; then :; else proof_status=$?; cat \"$proof_dir/output\"; exit \"$proof_status\"; fi; cat \"$proof_dir/output\"; for proof_scenario in policy workflows docs candidate transaction; do rg -F -q -- \"RELEASE_DISTRIBUTION=$proof_scenario STATUS=passed\" \"$proof_dir/output\" || exit 1; done; printf '%s\\n' 'PROJECT_IDENTITY=release-suite STATUS=passed SCENARIOS=5'"]
        expect_output: "PROJECT_IDENTITY=release-suite STATUS=passed SCENARIOS=5"
        timeout: 90m
        covers: ["R8.AC1", "R8.AC2", "R8.AC3", "R8.AC4", "R8.AC5", "R5.AC1", "R5.AC2", "R5.AC3", "R7.AC1", "R7.AC5", "R7.AC6", "R10.AC1", "R12.AC2", "R12.AC3", "NFR2", "NFR3", "NFR4", "C1", "C4", "C7"]

  - [ ] 4.7 Close the identity audit, preserve fresh evidence, and prepare the complete maintainer handoff
    - Scope: Run the final whole-repository identity gate, positive identity checks, isolated negative cases, and historical hash comparison. Complete the durable verification report under this feature with actual commands/outcomes, regenerated artifact paths, classified residue counts/reasons, commit boundaries, selected-feature evidence scope, and manual post-merge actions. The delivery check must reject any required check recorded failed/unrun or any operational residue, and must verify coherent specification-first commits. Do not claim legacy-portfolio certification or a public release. Commit final report/evidence in one additional verification commit only if needed for honest reviewability. The CLI evidence refresh and scoped release verdict are performed after task completion as the delivery checkpoint below, never recursively inside this task proof.
    - Requirements: `R8.AC5`, `R10.AC1`, `R10.AC2`, `R10.AC3`, `R10.AC4`, `R10.AC5`, `R10.AC6`, `R11.AC1`, `R11.AC2`, `R11.AC3`, `R11.AC4`, `R11.AC5`, `R11.AC6`, `R12.AC1`, `R12.AC2`, `R12.AC3`, `R12.AC4`, `R12.AC5`, `R12.AC6`, `NFR2`, `NFR3`, `NFR4`, `NFR5`, `C6`, `C7`, `C8`, `C9`
    - Design: Architecture / Durable Identity Verification; Architecture / Current Contracts, History, And Migration Documentation; Verification Plan
    - Verification:
      - command: ["./hack/verify-project-identity.sh", "all"]
        expect_output: "PROJECT_IDENTITY=all STATUS=passed"
        timeout: 20m
        covers: ["R8.AC5", "R10.AC1", "R10.AC2", "R10.AC3", "R10.AC4", "R10.AC5", "R10.AC6", "R11.AC1", "R11.AC2", "R11.AC3", "R11.AC4", "R11.AC5", "R11.AC6", "R12.AC2", "R12.AC3", "NFR2", "NFR3", "NFR4", "NFR5", "C7", "C9"]
      - command: ["./hack/verify-project-identity.sh", "audit-acceptance"]
        expect_output: "PROJECT_IDENTITY=audit-acceptance STATUS=passed"
        timeout: 10m
        covers: ["R11.AC4", "R11.AC5", "R11.AC6", "R12.AC2", "R12.AC5", "NFR5"]
      - command: ["./hack/verify-project-identity.sh", "delivery"]
        expect_output: "PROJECT_IDENTITY=delivery STATUS=passed"
        timeout: 10m
        covers: ["R12.AC1", "R12.AC3", "R12.AC4", "R12.AC5", "R12.AC6", "R10.AC6", "NFR2", "NFR3", "NFR4", "NFR5", "C6", "C7", "C8", "C9"]

## Delivery Checkpoint

After all leaves and their parent groups complete through the CLI, finish
all requested source/documentation/report/evidence changes and local commits.
Refresh the selected migration evidence once with
`walden verify project-identity-rename --json`; inspect actual bindings,
freshness, execution integrity, warnings, and any real proof re-executions.
Use a further scoped refresh only when final changes/failures make it needed.
Do not refresh or rewrite historical ledgers.

Run `walden release check project-identity-rename --strict --json` against
the final committed migration inputs. This is a selected-feature readiness
verdict and does not publish or certify the preserved legacy portfolio.
Do not waive pending or failed work. If any required proof, identity audit,
freshness/integrity check, or strict delivery verdict fails, report the
migration as incomplete with the concrete unresolved issue.

The final user report covers the specification, all major identity changes,
generated artifacts, exact executed verification/results, every remaining
old-name class and reason, and the manual GitHub/remote/profile/GHCR/release/
Artifact Hub actions. Repository rename and v0.2.0 publication remain
post-merge maintainer actions.
