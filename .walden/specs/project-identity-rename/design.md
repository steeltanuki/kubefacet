---
walden_schema_version: v1alpha1
status: approved
approved_at: 2026-09-26T11:43:39Z
last_modified: 2026-09-26T11:43:39Z
approved_fingerprint: sha256:920f58501881f319cd87010fcb2e02028ef4e00e513dc4c2bc833cfa4e88c31d
source_requirements_approved_at: 2026-09-26T11:34:28Z
source_requirements_fingerprint: sha256:0c36c66a6085389af6adf24c7c2963b2318e964b6abc515a952fdb726778c93b
---

# KubeFacet Project Identity Migration Design

## Architecture

This feature performs one coordinated, intentionally breaking identity
migration. It retains the production module boundaries, processing pipeline,
security model, and lifecycle state machines. It introduces no compatibility
API, migration controller, conversion webhook, or alternate installation path.

The approved requirements are authoritative. The baseline implementation is
commit `a09dc37581dbbe632d28022c384cf90521d5929d`, inventoried before source edits
in `identity-inventory.md`. The individual historical file identities are
recorded in `historical-identity-records.json`; this file is an inventory,
not execution evidence.

### Authoritative Identity Mapping

Brand text and resource names have different mappings. References to the
project become KubeFacet; references to the primary resource become Facet.
Go identifiers containing the resource name receive the corresponding Facet
prefix. Project-specific runtime names receive the lowercase kubefacet
prefix. Each occurrence is classified before editing its category.

| Identity | Baseline | Target |
| --- | --- | --- |
| Project brand | `Kubeseer` | `KubeFacet` |
| Canonical repository and module | `github.com/steeltanuki/kubeseer` | `github.com/steeltanuki/kubefacet` |
| Kubernetes API group/version | `kubeseer.io/v1alpha1` | `kubefacet.steeltanuki.it/v1alpha1` |
| Main Kind and Go type | `Kubeseer` | `Facet` |
| Main plural and singular | `kubeseers`, `kubeseer` | `facets`, `facet` |
| Main CRD | `kubeseers.kubeseer.io` | `facets.kubefacet.steeltanuki.it` |
| Main API source | `api/v1alpha1/kubeseer_types.go` | `api/v1alpha1/facet_types.go` |
| Main API test source | `api/v1alpha1/kubeseer_envtest_test.go` | `api/v1alpha1/facet_envtest_test.go` |
| Policy Kind and Go type | `KubeseerAccessPolicy` | `FacetAccessPolicy` |
| Policy plural and singular | `kubeseeraccesspolicies`, `kubeseeraccesspolicy` | `facetaccesspolicies`, `facetaccesspolicy` |
| Policy CRD | `kubeseeraccesspolicies.kubeseer.io` | `facetaccesspolicies.kubefacet.steeltanuki.it` |
| Policy API source | `api/v1alpha1/kubeseer_access_policy_types.go` | `api/v1alpha1/facet_access_policy_types.go` |
| Policy singleton | `installation-access-ceiling` | unchanged |
| Main executable and source directory | `kubeseer`, `cmd/kubeseer` | `kubefacet`, `cmd/kubefacet` |
| Local helper and source directory | `kubeseer-local`, `cmd/kubeseer-local` | `kubefacet-local`, `cmd/kubefacet-local` |
| Purge helper and source directory | `kubeseer-purge`, `cmd/kubeseer-purge` | `kubefacet-purge`, `cmd/kubefacet-purge` |
| Uninstall script | `hack/uninstall-kubeseer.sh` | `hack/uninstall-kubefacet.sh` |
| Chart directory, name, helper prefix | `charts/kubeseer`, `kubeseer`, `kubeseer.*` | `charts/kubefacet`, `kubefacet`, `kubefacet.*` |
| Default release and Deployment | `kubeseer` | `kubefacet` |
| Default namespace | `kubeseer-system` | `kubefacet-system` |
| Manager image | `ghcr.io/steeltanuki/kubeseer` | `ghcr.io/steeltanuki/kubefacet` |
| Helm OCI chart | `oci://ghcr.io/steeltanuki/charts/kubeseer` | `oci://ghcr.io/steeltanuki/charts/kubefacet` |
| Project environment namespace | `KUBESEER_*` | `KUBEFACET_*` |
| Project metric prefix | `kubeseer_*` | `kubefacet_*` |
| Owned label/annotation domain | `kubeseer.io/*` | `kubefacet.steeltanuki.it/*` |
| Default kind cluster and context | `kubeseer-local`, `kind-kubeseer-local` | `kubefacet-local`, `kind-kubefacet-local` |
| Default persistent state/cache | `.local/state/kubeseer/local`, `.cache/kubeseer/local` | `.local/state/kubefacet/local`, `.cache/kubefacet/local` |
| Current chart/application version | `0.1.6` | `0.2.0` |
| Example resource manifests | `examples/*/kubeseer.yaml` | `examples/*/facet.yaml` |

Nested public API types are renamed consistently, including source, field,
operator, aggregation, provenance, match, value, result, error, and state
types. Associated constants, store interfaces, adapters, predicates,
validators, webhook helpers, and identity-bearing local variables receive
the matching resource name. Generic names such as Source, View, Resource,
Observer, Pipeline, Result, and Runtime retain their existing meaning.

### API, Admission, And Runtime Coupling

Update `api/v1alpha1/doc.go`, `groupversion_info.go`, and resource markers
first, then consumers in `internal/`, `cmd/`, and `test/`. Scheme registration
contains only Facet, FacetList, FacetAccessPolicy, and FacetAccessPolicyList
for the new group. Main resources remain namespaced; policy remains
cluster-scoped; storage and served version remain v1alpha1. JSON tags,
field defaults, validation constraints, status subresources, condition/reason
codes, and authorization boundaries remain unchanged.

The main admission path is
`/validate-kubefacet-steeltanuki-it-v1alpha1-facet`; the policy path is
`/validate-kubefacet-steeltanuki-it-v1alpha1-facetaccesspolicy`. The webhook
names are `facet.kubefacet.steeltanuki.it` and
`facetaccesspolicy.kubefacet.steeltanuki.it`. Both source registration and
Helm rules target the new group and resource plurals. Preserve failurePolicy
Fail, matchPolicy Exact, admission review v1, sideEffects None, timeouts,
operation sets, and existing validation outcomes.

Default package names become `kubefacet`, `kubefacet-webhook`,
`kubefacet-validating-webhook`, and their existing resource suffixes.
Helm fullname/custom namespace behavior remains intact. Certificate resources,
Secret references, mounted paths, DNS names, manager defaults, and hook flags
all derive the same Service and namespace. Defaults include
`/var/run/secrets/kubefacet/webhook` and
`/var/run/secrets/kubefacet/ca/ca.crt`; certificate/key basenames are unchanged.

Rename `ExpectedKubeseerCRDStorageVersion` and its CLI flag to
`ExpectedFacetCRDStorageVersion` and `--expected-facet-crd-storage-version`.
Readiness and preflight continue checking the same storage contract against
the newly named CRD. The purge confirmation becomes
`purge-kubefacet-crds`; exact confirmation and ownership checks remain
mandatory. The new purge tool cannot target old-group resources.

Controller/Event component `kubeseer-reconciliation-runtime` becomes
`kubefacet-reconciliation-runtime`; the default leader-election ID becomes
`kubefacet-controller`. Update manager/logger names, typed watches,
Event reporters, field managers, and lifecycle selectors together. Standard
Kubernetes labels and upstream kind ownership labels keep their keys;
project values such as `app.kubernetes.io/name` and `part-of` become kubefacet.
Owned release/namespace/ownership keys use `kubefacet.steeltanuki.it/`.

No processing algorithm changes: events still enqueue owner identities;
reconciliation still performs fresh discovery/selection, authorizes every
read, preserves watch establishment versus stream lifetime, and publishes
only current semantic status.

### Environment, State, And Telemetry

Migrate every setting currently in the KUBESEER namespace to KUBEFACET,
including the 53 inventoried runtime/test/local/package setting tokens and
dynamically formed per-version variables. Trace producers and consumers
through Go lookups, shell expansion/export, Helm values, and workflow env.
Do not add fallback lookups for the old prefix.

Project-owned unprefixed environment settings discovered during the audit,
including release endpoint overrides, release SHA handoff, local identities,
and project-specific acceptance fault injection, also receive KUBEFACET
names. Standard tool/process variables such as HOME, XDG roots, TMPDIR,
GOCACHE, GOMODCACHE, GOPROXY, KUBECONFIG, GitHub-provided variables, and
KIND_EXPERIMENTAL_PROVIDER retain upstream meanings. Neutral Make inputs
such as SCENARIO, EXAMPLE, ACTION, KUBERNETES_VERSION, and declared toolchain
version variables remain Make arguments; project-specific script settings
are exported under the new namespace. Internal shell constants are not
environment interfaces merely because they use uppercase names.

State, cache, generated diagnostic bundle, temporary fixture, local image,
registry fixture, and OCI archive defaults use kubefacet. Honor explicit
existing override semantics and absolute-path validation. Do not move,
reuse, remove, or silently adopt old persistent state. The filesystem path
of this checkout and the Git remote remain maintainer-managed boundaries.

Rename all nine metric families, preserving collector type and labels:

| Target metric | Type | Existing labels |
| --- | --- | --- |
| `kubefacet_reconciliations_total` | Counter | outcome, reason |
| `kubefacet_reconciliation_duration_seconds` | Histogram | outcome |
| `kubefacet_resources_read_total` | Counter | scope |
| `kubefacet_source_failures_total` | Counter | stage, reason |
| `kubefacet_results_produced_total` | Counter | outcome |
| `kubefacet_status_updates_total` | Counter | outcome, reason |
| `kubefacet_authorization_decisions_total` | Counter | kind, outcome, reason |
| `kubefacet_jsonpath_failures_total` | Counter | reason |
| `kubefacet_source_watch_restarts_total` | Counter | reason |

Preserve histogram buckets, finite vocabularies, registration/rollback
behavior, synchronous observation points, Event emission rules, and
sensitive-value protection. Update metric assertions and probes without
altering increments or observation counts. Trace instrumentation uses the
new module path; spans/attributes and project-specific correlation keys use
kubefacet or Facet according to their project/resource role.

### Packaging, Generation, And Distribution

Move the chart and rename every helper namespace, include call, rendered
name, owned selector, annotation, schema description, and image default.
Set chart/application versions to 0.2.0. Set the exact requested description
and all five keywords. Preserve the range `>=1.35.0-0 <1.37.0-0`, matrix
1.35.6/1.36.2, pinned node images, architecture, dependencies, container
security, TLS modes, RBAC permissions, policy hooks, and lifecycle ordering.

Generation sequence is `make generate`, `make manifests`, then
`make package-sync-crds`. The source CRDs become
`config/crd/bases/kubefacet.steeltanuki.it_facets.yaml` and
`config/crd/bases/kubefacet.steeltanuki.it_facetaccesspolicies.yaml`.
Remove obsolete generated CRDs explicitly; never patch them into the new
identity. Chart CRD copies use those same filenames and bytes.

Extend the existing package sync workflow to derive both SHA-256 values and
update only the generated checksum annotations in Chart.yaml:
`kubefacet.steeltanuki.it/generated-crd-facet-sha256` and
`kubefacet.steeltanuki.it/generated-crd-access-policy-sha256`. Read-only
verification regenerates into an isolated directory and compares outputs,
copies, and checksum metadata. It never repairs drift during proof execution.

The container builds and launches /kubefacet; OCI labels use KubeFacet and
the canonical repository. Release scripts and workflows target the new
image/chart/repository identities, release lock/temporary names, archive
paths, and metadata markers. Add `docs/releases/v0.2.0.md` as source release
metadata with the identity break and verification boundary, because source
preflight requires a version-matching note. This prepares a future release;
it does not create a tag or publish artifacts.

Disposable release fixtures move their synthetic versions from the old
line to the 0.2.x line. Keep retry, partial-publication recovery, digest
conflicts, anonymous retrieval, workflow rejection, source lineage, exact
gated SHA, protected tag, and immutable-candidate assertions intact. Never
invoke publication against production endpoints during this migration.
Ordinary CI retains read-only hosting permissions and cannot publish.

### Local Development And Examples

The persistent environment retains its existing state machine, Podman
provider, ownership metadata format, explicit kubeconfig, loopback
validation, readiness gates, resume rules, and bounded deletion behavior.
Only the names/settings change. Genuine verification uses dedicated
absolute state/cache roots and owned clusters; it must not access a
previous Kubeseer installation. Acceptance fixtures and expectation strings
change together so they keep proving the same rejection and cleanup cases.

Rename the seven current example resource manifests to facet.yaml and
update their kinds, groups, names, namespaces, references, and selectors.
Project-owned custom fixture API domains become the corresponding
`fixtures.kubefacet.steeltanuki.it` domain. Preserve ordinary Kubernetes
resource contents and all extraction/operator/aggregation/denial semantics.
Local example verification and full E2E certification exercise those results.

Readiness and diagnostics continue using EndpointSlices, not legacy
Endpoints. Confirm that Service selectors, app labels, typed probe clients,
local helper paths, E2E resource polling, sentinel values, and cleanup agree
on the new identity. Do not reinterpret a sandbox-denied Podman runtime as
a passing genuine-cluster test.

### Current Contracts, History, And Migration Documentation

Create `.walden/current-identity.md` as a current contract overlay linking
this reviewed specification and the older feature contracts. It maps their
identity-dependent clauses to the new identifiers, retains their surviving
semantics, and identifies the renamed canonical regression checks. Update
the constitution, SPECIFICATIONS, active checks, and current documentation
to refer to that overlay. Historical feature directory identifiers remain
stable; references to them are explicitly labeled historical feature IDs.

Preserve all individually inventoried historical specification/evidence,
lesson, and release-note bytes. Do not reconcile or reapprove those old
documents, backfill their ledgers, retire them, or replay obsolete one-time
bootstrap/publishing proofs. Their evidence may be stale against the new
tree and is not KubeFacet certification. Current implementation evidence is
recorded under project-identity-rename, using the renamed regression checks.
A selected-feature release verdict must be reported as selected-feature.

The mixed `docs/release-pipeline-audit.md` needs occurrence-level treatment:
dated v0.1.x observations and historical run links remain facts; present-tense
package/installation guidance uses the new identity. Label its historical
context and keep its unimplemented automation proposal explicitly a proposal.
CONTRIBUTING retains optional Walden usage and the existing maintainer model.

Add concise `docs/migration-from-kubeseer.md` and link it from current
installation/README/release documentation. Describe the version boundary,
API/Kind/module/environment/metric/package mappings, unsupported old-to-new
Helm upgrade, lack of CRD conversion, explicit removal of the old installation,
and clean new installation. Link old lifecycle documentation/tooling at the
immutable v0.1.6 tag; the administrator follows its original ownership and
destructive-confirmation requirements. Historical releases remain available.
No new KubeFacet cleanup tool accepts old-group targets.

Document manual post-merge repository rename, local remote update, GitHub
description/topics/social preview review, GHCR visibility review, future
v0.2.0 publication, and later Artifact Hub registration. No hosted repository
rename, remote edit, public push/tag/release, or package deletion occurs here.

### Durable Identity Verification

Add a read-only repository identity checker, exposed through
`hack/verify-project-identity.sh` and included in `make verify`. It scans
current tracked and non-ignored source files, including hidden files and the
entire Walden tree, for case-sensitive and case-insensitive old-name matches
and identity-bearing paths. Git metadata and ignored build/cache outputs are
not source contracts. Explicitly inspect actual built/rendered artifacts in
the corresponding package/runtime checks as well.

Classify matches with two bounded mechanisms:

1. Historical exemptions name exact inventoried files and their baseline
   hashes. New files and additions to existing historical files are not
   automatically exempt. The 98-record baseline protects historical files
   even if they do not contain an old-name match.
2. Migration explanations and historical references in active documents use
   exact path plus matching-line digest/count and a short reason. This covers
   the new migration specification/inventory, explicit old-to-new mappings,
   immutable old release URLs, and historical feature ID links. It does not
   exempt a whole current document or the whole Walden directory.

Store reviewed exceptions in a migration policy data file alongside the new
specification. References containing forbidden text can be encoded in
exception selectors so that the exception file does not recursively exempt
its own contents; the checker reports decoded file/line locations and reasons.
Baseline historical inventory metadata is itself classified as migration
documentation. Construct the detector's obsolete tokens from fragments so
the checker and its negative fixtures do not require operational exemptions.
Never auto-accept new matches or silently update a historical hash.

Fail on unclassified text/path matches, invalid or overly broad exception
selectors, changed preserved bytes, and new operational references inside
otherwise allowed active files. Emit a nonempty classified occurrence report
and an explicit success marker only after checking the complete scope.

Exercise the gate against isolated copies or a temporary source fixture,
not by editing/restoring the real worktree. Include obsolete imports, API
groups/Kinds, environment settings, metric names, chart/runtime selectors,
mixed case, path-only residue, a newly added Walden contract, and an old
identifier appended to a mixed historical/current document. Preserve
positive checks for each deliberate historical/migration class.

Supplement the residue gate with positive identity assertions. Verify exact
GroupVersion/scheme/resource identity, webhook rules, default names/SANs,
module/executables, environment producers/consumers, nine metric families,
chart metadata/images, examples, and release fixtures. A clean residue scan
alone is insufficient because a mistyped new identity would also be clean.

### Generated Schema And Semantic Baselines

Capture a self-contained baseline of the old generated API schema before
renaming sources, with baseline commit/source hashes and resource mapping.
The comparison retains serialized fields, required sets, defaults, types,
enums, nullable flags, numeric/cardinality limits, CEL validations,
subresources, scopes, served/storage versions, and printer columns. It
normalizes only intended resource/group/name identity and descriptive prose.
Record the normalization rules explicitly; do not discard behavioral schema
constraints to make comparison pass. Baseline capture is migration data,
not a claim that new code has been executed.

Compare new generated APIs/CRDs and deepcopy behavior against that baseline.
Existing integration/envtest/E2E assertions remain the semantic regression
contract, with identity substitutions only. Add focused integration assertions
for new scheme and runtime/package identities where the existing cases do
not already assert them. No package-local unit-test layer or unrelated
implementation refactoring is introduced.

## Options Considered

The chosen approach is a clean rename coordinated across API, runtime,
packaging, tests, and current contracts, with an explicit historical overlay.
It matches the requested alpha-stage breaking boundary and avoids a second
resource/installation lifecycle.

A dual-group compatibility layer would require conversion/defaulting,
admission and authorization coordination, separate discovery/watch paths,
metric/environment aliases, and lifecycle policy for both identities. It
would preserve a public contract the maintainer explicitly chose to remove
and is rejected.

A global replacement would confuse brand and Kind, leave generated artifacts
unproven, and rewrite historical evidence. It is rejected. Focused mechanical
edits are useful only after categorization and with reviewed mappings.

Rewriting every old specification and refreshing all old evidence would break
approval provenance and replay historical delivery tasks. The explicit current
identity overlay and new migration evidence provide a smaller, truthful
solution. Historical records remain recoverable and are not retired.

## Simplicity And Elegance Review

The production design stays intact. New machinery is limited to identity
verification, reviewed exception data, a schema baseline comparison, and
existing generation/checksum synchronization. There is one served API
group, one chart identity, one environment namespace, and one set of metrics.

Names flow through existing module and Helm interfaces. No shared production
identity abstraction is introduced merely to centralize strings: it would
couple independently maintained API, packaging, and harness layers. Positive
cross-layer assertions detect disagreement instead.

The first-draft simplification review rejected a new general migration tool,
automatic rewriting of installations, and a separate historical portfolio
state machine. Existing CLI review/evidence mechanics plus a current contract
overlay are sufficient. The audit exemptions remain narrowly reviewable
data; negative scenarios verify that they cannot hide new active contracts.

## Failure Modes And Tradeoffs

| Failure or tradeoff | Containment and verification |
| --- | --- |
| Brand text becomes a resource name, or vice versa | Apply separate KubeFacet/Facet mappings; inspect Go public identifiers and documentation context. |
| New Go names compile while old API is still served | Check GroupVersion, scheme, markers, CRD discovery, resource plurals, and absence of aliases. |
| A renamed generated file hides schema changes | Regenerate canonically, compare semantic schema baseline, and execute real API contract/admission tests. |
| Helm registers a different path/SAN from the manager | Assert rendered configuration against production defaults; exercise both certificate modes and real admission. |
| Ownership or readiness selector misses the new workload | Cross-check Helm selectors, lifecycle clients, EndpointSlice probes, E2E observation, and cleanup. |
| Cleanup reaches an old or unrelated installation | New-group clients, exact release/namespace ownership, isolated explicit kubeconfigs, exact destructive confirmation, and existing rejection tests. |
| Environment producer is renamed but consumer is not | Enumerate lookup/export pairs, dynamic version suffixes, workflow handoff, and harness fault cases. |
| Metric rename changes observation semantics | Retain collector shape, labels, vocabularies, bucket configuration, and existing count/event assertions. |
| Old CRDs survive beside regenerated new CRDs | Explicitly remove obsolete generated outputs and verify exact expected CRD sets and chart copies. |
| Chart checksum or source note blocks the future release | Derive hashes in sync, assert read-only consistency, and supply source metadata for v0.2.0. |
| Disposable release fixture accidentally targets production | Keep local-endpoint authorization/restrictions, owned registry fixtures, and mutation/recovery assertions; do not run public publishing. |
| Historical file exclusion hides newly added code | Bind exact historical files/bytes, use line-level active-document exceptions, and inject negative cases into isolated copies. |
| Old proofs fail after command/path changes | Preserve them as historical evidence; certify the renamed current regression contract through the migration feature. Do not claim a full legacy-portfolio verdict. |
| Sandbox denies Podman or envtest listeners | Use authorized execution with the required runtime access; report failures/unrun genuine checks rather than replacing them with fake-tool success. |
| Required verification is slow or intermittently fails | Run isolated suites sequentially where they share clusters/resources; inspect the actual failure, rerun the same final tree when justified, and preserve failed attempts. |
| Existing users require manual reinstall | Accept the intentional alpha-stage break; document old-version uninstall/purge and unsupported in-place upgrade. No automatic old-state adoption. |

The historical record retains old names by design. This is acceptable only
with explicit supersession, matching bytes/reasons, and a final report that
distinguishes history from current contracts and current execution evidence.

## Verification Plan

Verification is layered and non-vacuous. Each implementation task proves its
own new identity assertions before completion; the final checkpoint runs the
full requested repository scope against the final source tree. Proofs are
read-only: generation/build outputs go to isolated directories, local/cluster
tests capture worktree snapshots, and no proof edits exception data or fixes
checksums. Commands must emit their named pass markers or named Go PASS
records, not merely exit successfully with zero intended tests.

| Check | Required observation |
| --- | --- |
| `walden validate project-identity-rename --all --json` | All three reviewed phases valid, all requirement/design/task/proof references covered, no unresolved decisions. |
| `make generate`, `make manifests`, `make package-sync-crds` during implementation | New deepcopy/CRD outputs produced from sources; exact chart copies and derived checksum metadata. These are implementation actions, not re-verification proofs. |
| Read-only schema and positive identity checks | Exact new scheme/CRDs/public types/webhooks/defaults; baseline field/schema equivalence; no old aliases. |
| `make verify` | Generated consistency, architectural/testing boundaries, admission/observability/limits, E2E boundaries, package, local environment, and new repository identity gate all pass. |
| `make test` with noncached execution | Real module integration scenarios execute, including authorization, discovery, selection, extraction, typing, operators, aggregation, reconciliation/status, admission, metrics, packaging, and EndpointSlice probes. |
| `make test-compatibility` | API contract, discovery, selection, reconciliation/status Events, and admission pass against envtest Kubernetes 1.35.6 and 1.36.2. |
| `make test-package-compatibility` | Deterministic chart renders for both supported Kubernetes versions and both certManager/externalSecret modes retain fail-closed and secure lifecycle contracts. |
| Genuine package smoke profiles using the existing per-version kubeconfig/context interface under its new prefix | Dedicated owned kind-on-Podman clusters validate installation/removal, author RBAC, policy bootstrap, webhook/certificate modes, upgrade/rollback, uninstall, and confirmed purge. No ambient cluster fallback. |
| `./hack/e2e-harness-acceptance.sh` | Owned-cluster isolation, exact identities, explicit kubeconfig/context, readiness, diagnostics, failure handling, and cleanup assertions pass. |
| `make e2e KUBERNETES_VERSION=1.35.6` and `make e2e KUBERNETES_VERSION=1.36.2` | All existing certification scenarios execute on each supported owned Podman cluster, including observable authorization/admission/status/metrics and lifecycle results. |
| `make local-check`, `make test-local-environment`, `make test-local-cluster-resume` | Working rootless Podman; genuine local/example/diagnostic proof and owned exited-node resume with retained workload/container identity. Require genuine markers, not just fake-tool fallback markers. |
| `make test-release-distribution SCENARIO=all` | All five source-policy, candidate, publication-transaction, workflows, and documentation scenarios pass using owned local registries/endpoints, including recovery and immutable conflicts. |
| Read-only manager/helper builds and Go module consistency | All renamed executable paths build; version metadata is correct; `go mod tidy -diff` reports no module drift without modifying source. |
| Case-sensitive and case-insensitive repository residue audit, including hidden/Walden files and paths | Zero unclassified/operational obsolete identity; every remaining occurrence has an individually reviewable historical/migration reason. |
| Negative audit acceptance and final historical hash comparison | Newly injected obsolete references fail in each category; historical byte integrity remains intact. |
| `walden verify project-identity-rename` and scoped `walden release check project-identity-rename` | Completed tasks have current bound evidence and an honestly scoped delivery verdict after final code/docs/commits. No release publication or legacy-portfolio certification claim. |

Use supported toolchain inputs from `hack/toolchain.mk`, writable Go
build/module caches under new project paths, pinned envtest assets, and
explicit Podman/kind prerequisites. Assign justified longer timeouts to full
matrix, cluster, and release-distribution proofs in the task plan. A passing
fake-tool acceptance test supplements genuine verification; it cannot replace
the required genuine test.

Stages/commits remain logically reviewable: specification first; API/module/
runtime and their tests; packaging/distribution/local harnesses and generated
metadata; documentation/current contracts and final evidence. Additional
closely related verification commits are acceptable. Intermediate stages may
require identity-aware focused checks before the final cross-layer gate;
record that scope honestly instead of claiming full completion early.

The completion report names the new specification, all major identity
changes, regenerated artifacts, exact executed commands/results, every class
of remaining old-name reference, and manual post-merge actions. Any failed,
unrun required check or operational residue makes the migration incomplete.

## Requirement Coverage

| Requirement | Covered By |
| --- | --- |
| `R1` | Identity-only architecture and generated-schema baseline; original module/envtest/compatibility/E2E assertions retain all six semantic boundaries, including lifecycle and telemetry. |
| `R2` | Authoritative API/type mapping, scheme/markers, policy singleton, coupled admission registrations, canonical generation, schema comparison, API discovery and admission tests; covers all seven criteria. |
| `R3` | Module/import, API/command/script path mapping, container/build/helper consumers, public symbol audit, read-only builds/module consistency; covers all four criteria. |
| `R4` | Runtime names, owned-domain mapping, certificate SAN/path alignment, controller/lease/Event/field-manager identifiers, selectors, CLI/diagnostics, positive render/lifecycle/probe assertions; covers all five criteria. |
| `R5` | Environment producer/consumer enumeration, full project-owned namespace mapping, no old fallbacks, independent new state/cache/temp roots and genuine harness checks; covers all three criteria. |
| `R6` | Nine-collector table with fixed types/labels, no old registration, new trace/correlation identifiers, existing count/confidentiality assertions and metric exposition; covers all three criteria. |
| `R7` | Chart mapping, exact description/keywords, retained Kubernetes range/matrix, release/namespace/image defaults, canonical generation and checksum/copy comparison; covers all eight criteria. |
| `R8` | 0.2.0 chart/application/source-note preparation, canonical image/OCI destinations, unchanged protected-tag/exact-SHA/immutable publication gates, disposable transactions, no public/history mutation; covers all five criteria. |
| `R9` | Owned Podman local/context/state identity, acceptance/resume/E2E coupling, seven renamed example manifests and unchanged example verification outcomes; covers all five criteria. |
| `R10` | Current documentation and contract overlay, preserved README positioning/contributor model, explicit breaking-migration document, immutable old lifecycle links, complete manual post-merge checklist; covers all six criteria. |
| `R11` | Exact historical hashes, explicit identity supersession, active contract/check updates, whole-source text/path audit with bounded exceptions and negative injection, canonical verify integration; covers all six criteria. |
| `R12` | Reviewed pre-implementation chain, retained behavioral test assertions, full layered final verification, coherent commits and fresh feature evidence, explicit incomplete verdict on gaps, complete handoff; covers all six criteria. |
| `NFR1` | Unchanged processing architecture, schema-equivalence comparison, original security/determinism/status/limit assertions across real integration and cluster layers. |
| `NFR2` | Canonical generators and sync, isolated read-only regeneration/build proofs, named test/marker checks, supported toolchain/matrix and bounded proof execution. |
| `NFR3` | Historical byte inventory, current identity overlay, immutable old release references, no legacy evidence rewriting and clearly scoped current evidence. |
| `NFR4` | Independent project state, explicit owned kubeconfigs/clusters, Podman provider, lifecycle confirmation/ownership rules, local-only release fixtures and unchanged publication safety gates. |
| `NFR5` | Category-specific mappings, occurrence-level audit explanations, reviewable stage/commit boundaries, scoped evidence and explicit post-merge handoff. |
