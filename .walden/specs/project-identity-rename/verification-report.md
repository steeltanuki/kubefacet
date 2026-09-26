# KubeFacet Identity Migration Verification Report

## Scope and evidence boundary

This report covers the selected feature `project-identity-rename` only; the
evidence boundary is selected feature only, and it is not portfolio-wide certification.
The approved fingerprints are:

- Requirements: `sha256:0c36c66a6085389af6adf24c7c2963b2318e964b6abc515a952fdb726778c93b`
- Design: `sha256:920f58501881f319cd87010fcb2e02028ef4e00e513dc4c2bc833cfa4e88c31d`
- Tasks: `sha256:a33b0f23bbdc1596f46ab185b22593430af89fbb51a6b0012ff0480f510ece84`

The final implementation and delivery-gate commit before this report is
`ffc52b811f6cbdcf52ba97841abac4e151ec61fa` (`test: certify KubeFacet package
lifecycle`). Selected-feature execution records are in
`.walden/evidence/project-identity-rename.json`. Exact declared proof argv,
expected and actual exit codes, and output digests are retained in each task's
evidence steps. Historical feature evidence remains byte-for-byte unchanged
and is not used as current execution evidence; legacy feature evidence
remains historical. No public push, tag, release,
package publication, hosted repository rename, or legacy-portfolio claim is
part of this result.

## Declared checkpoints and actual outcomes

The table records each completed task's final result and named marker. The
evidence ledger retains the exact proof command arrays for all steps. The
final audit row records the three task 4.7 commands after each was executed
successfully.

| Task | Command set | Marker or outcome | Result |
| --- | --- | --- | --- |
| 1.1 | Approved baseline provenance Python proof | `PROJECT_IDENTITY=specification STATUS=passed BASELINE_RESOURCES=2` | PASS |
| 1.2 | `./hack/verify-project-identity.sh history`; `./hack/verify-project-identity.sh audit-acceptance` | 98 historical records and two baseline resources verified; 11 negative cases rejected | PASS |
| 2.1 | Identity API check, named `ProjectIdentityAPI` module test, renamed binary builds | API schema semantic equivalence; module test and three builds passed | PASS |
| 2.2 | Runtime identity check, named `ProjectIdentityRuntime` module test, admission boundary proof | Runtime contracts and admission boundaries passed | PASS |
| 2.3 | Observability identity check, named integration tests, observability boundary proof | Nine metric families and structured observer identity passed | PASS |
| 3.1 | Generated-artifact, package identity, and render compatibility proofs | Both Kubernetes versions and both certificate modes rendered successfully | PASS |
| 3.2 | Release identity, release policy, and workflow distribution scenarios | Policy and workflow scenarios passed | PASS |
| 3.3 | Environment/local identity checks and local/E2E harness acceptance | Seven examples and owned local/E2E identities passed deterministic acceptance | PASS |
| 4.1 | Docs, history, repository audit, and isolated audit acceptance | Current docs contracts, 98 historical hashes, and 11 negative cases passed | PASS |
| 4.2 | `make verify`; `make test GO_TEST_FLAGS=-count=1`; `make test-compatibility GO_TEST_FLAGS=-count=1 KUBERNETES_COMPATIBILITY_VERSIONS='1.35.6 1.36.2'`; `make test-package-compatibility`; renamed builds; `go mod tidy -diff` | Canonical verification, noncached module integration, both API versions, both render modes, three builds, and module consistency passed | PASS |
| 4.3 | `make local-check`; `make test-local-environment`; `make test-local-cluster-resume` | `LOCAL_ENVIRONMENT=check STATUS=passed`; genuine EndpointSlice and owned-node resume markers passed | PASS |
| 4.4 | `./hack/test-project-identity-package.sh` | `PROJECT_IDENTITY=package-cluster STATUS=passed PROFILES=4` | PASS |
| 4.5 | `./hack/e2e-harness-acceptance.sh`; `make e2e KUBERNETES_VERSION=1.35.6 GO_TEST_FLAGS=-count=1`; `make e2e KUBERNETES_VERSION=1.36.2 GO_TEST_FLAGS=-count=1` | All 15 E2E scenarios passed on both versions; both suites reported `--- PASS: TestEndToEnd` | PASS |
| 4.6 | `make test-release-distribution SCENARIO=all` with the declared output capture and marker assertions | `PROJECT_IDENTITY=release-suite STATUS=passed SCENARIOS=5` | PASS |
| 4.7 | `./hack/verify-project-identity.sh all`; `./hack/verify-project-identity.sh audit-acceptance`; `./hack/verify-project-identity.sh delivery` | `PROJECT_IDENTITY=all STATUS=passed`; `PROJECT_IDENTITY=audit-acceptance STATUS=passed rejected_scenarios=11 positive_classes=2`; `PROJECT_IDENTITY=delivery STATUS=passed` | PASS |

The final aggregate identity gate reported history `records=98`, API schema
`RESOURCES=2`, three renamed executable builds, seven examples, and a whole-
repository audit with `occurrences=1487 unclassified=0 files=393`. It also
passed the release, runtime, observability, package, documentation, and local
identity checks. The standalone negative audit acceptance reported
`rejected_scenarios=11 positive_classes=2`. The final report includes the
historical SHA-256 comparison and isolated negative-injection cases.

Two initial task 4.4 attempts exposed proof-script defects: the first Facet
fixture failed before semantic admission, and the next attempt used a Helm
uninstall flag Helm does not support. The fixture now reaches the exact
semantic Kind violation and uninstall checks release state before repeating;
the final two-version, four-profile live run passed and cleaned its owned
clusters and image tag. Task 4.5's first preflight attempt used a task-specific
temporary directory that had not been created; after creating the isolated
cache/temp roots, the canonical harness and both genuine E2E suites passed.
These retries did not leave a required checkpoint failed.

## Regenerated artifacts

The canonical generators and synchronization workflow cover these committed
artifacts:

- `make generate` produces `api/v1alpha1/zz_generated.deepcopy.go`.
- `make manifests` produces `config/crd/bases/kubefacet.steeltanuki.it_facets.yaml`
  and `config/crd/bases/kubefacet.steeltanuki.it_facetaccesspolicies.yaml`.
- `make package-sync-crds` copies those two CRDs byte-for-byte into
  `charts/kubefacet/crds/`.
- `hack/verify-package.sh` verifies the CRD SHA-256 annotations in
  `charts/kubefacet/Chart.yaml` against the generated source bytes. The
  package proof also rendered and exercised the chart on both supported
  Kubernetes versions in both certificate modes.
- Release chart/image identity and consumer metadata are in
  `charts/kubefacet/Chart.yaml`, `charts/kubefacet/values.yaml`, and
  `docs/releases/v0.2.0.md`. Release-distribution scenarios used local
  disposable endpoints; no hosted image or chart was published.

The semantic schema comparison checked the generated CRDs against both
captured baseline resources after normalizing only reviewed identity fields.
Temporary manager/helper binaries were built under an isolated temporary
root and were not committed.

## Repository identity residue

Final audit: 393 source paths scanned, 1,487 individually classified audit
records, zero unclassified or operational residues. The audit acceptance
rejected 11 isolated negative-injection cases, including obsolete imports,
API identities, environment and metric names, selectors, mixed case, new
Walden contracts, path-only residue, changed allowlisted text, and changed
historical bytes.

Remaining classes and reasons:

- **Historical records:** 98 exact-hash records remain unchanged: 93 under
  `.walden/` and five historical release documents. They contain 1,345
  identity-bearing text lines with 1,808 matches, plus four historical path
  matches. These are approved old feature specifications/evidence and
  released-version records; rewriting them would falsify their history.
- **Migration explanations:** 137 exact line selectors across 16 files
  account for 167 matches. They retain current migration mappings, stable
  historical feature IDs in the active feature map, old-name context in the
  new migration specification, immutable release links, and dated release
  audit observations. Each line's SHA-256, match count, and reason are
  individually recorded in `identity-exceptions.json`.
- **Migration guide path:** one exact path selector keeps the breaking
  migration guide addressable from current docs. The path, content digest,
  and rationale are recorded in `identity-exceptions.json`.
- **Operational source, API, runtime, chart, workflow, local, and E2E
  identities:** zero remaining obsolete identifiers are accepted.

All 98 preserved historical file hashes and line inventories match the
pre-edit commit `a09dc37581dbbe632d28022c384cf90521d5929d`. No historical
ledger was refreshed or rewritten.

## Commit boundaries

The local branch retains specification-first order and related scopes:

1. `16acbb18972cc15723910411821af4755b6ec614` — `spec: define KubeFacet
   identity migration` (approved requirements, design, task plan, inventory,
   and immutable API baseline).
2. `5fdc81db0f007b95dee7dd13f87cde7d320bb476` — `refactor: rename
   Kubernetes API and runtime identity` (Go module/API types, generated
   schema, manager, admission, runtime, and behavioral tests).
3. `5c3b795503bfce4c97b0427b20293b47fea26150` — `build: rename KubeFacet
   packaging and distribution` (chart, release, environment, local/E2E,
   examples, and related harness identities).
4. `61631f16efbd0e3c4f8765f11f7dac86b0b5d8c1` — `docs: complete KubeFacet
   migration` (current contract, migration guide, historical links, and
   audit policy).
5. `346f54249374f20a67d08106b6552317d60fb5b6` — `test: certify KubeFacet
   package lifecycle` (owned two-version cluster wrapper, live package
   lifecycle smoke, audit aggregate/delivery modes, and task 4.2–4.6 evidence).

The final report and task 4.7 evidence are committed separately after the
task-completion CLI records the final audit results. The commits are local to
`refactor/kubefacet-rename`; they are not pushed.

## Manual actions after merge

Maintainer work outside this migration:

- Rename the GitHub repository to `kubefacet`.
- Update the maintainer's local Git remote after that hosted change.
- Review the GitHub description, topics, and social preview image.
- Confirm GHCR image and chart package ownership and visibility without
  mutating historical packages as part of this migration.
- Publish KubeFacet v0.2.0 later through the approved tag-gated release path.
- Register the project with Artifact Hub later.

The physical checkout path may retain its previous name. The repository
rename, remote update, profile changes, package review, v0.2.0 publication,
and Artifact Hub registration remain maintainer actions.

## Walden delivery checkpoint

This is a selected-feature verdict; it does not certify the preserved legacy
portfolio. This selected-feature verdict does not certify the preserved legacy portfolio.

- The first `walden verify project-identity-rename --json` refresh re-proved
  the stale tasks and reported `ok=false` at task 4.3. Its owned node resumed,
  but the canonical Helm pre-upgrade compatibility Job ended with
  `BackoffLimitExceeded`. Tasks 1.1–4.2 and 4.4–4.7 reported passing bindings
  and outcomes in that refresh.
- A standalone `make test-local-cluster-resume` retry passed with
  `LOCAL_CLUSTER_RESUME_ACCEPTANCE=genuine STATUS=passed` and cleaned its
  run-unique cluster.
- The follow-up `walden verify project-identity-rename --json` returned
  `ok=true`: `verification passed for project-identity-rename: 1 task(s)
  re-proven, 14 skipped as verified`. The refreshed task 4.3 binding is
  current and its verification integrity is `pure`.
- `walden evidence status project-identity-rename --json` reports 15
  verified tasks, no warnings, current task bindings and code freshness,
  passing assertions, and pure integrity for tasks 1.1–4.6; task 4.7 retains
  its passing `post-state` completion evidence.

The strict `walden release check project-identity-rename --strict --json`
result is recorded after running it against the final committed migration
inputs. A failed proof, stale or invalid evidence, unclassified operational
residue, or failed strict verdict means the migration remains incomplete.
