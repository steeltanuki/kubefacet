---
walden_schema_version: v1alpha1
status: approved
approved_at: 2026-09-26T11:34:28Z
last_modified: 2026-09-26T11:34:28Z
approved_fingerprint: sha256:0c36c66a6085389af6adf24c7c2963b2318e964b6abc515a952fdb726778c93b
---

# KubeFacet Project Identity Migration Requirements

## Introduction

Kubeseer v0.1.x is becoming KubeFacet starting with v0.2.0. This feature
changes project and API identity only. It is intentionally breaking: there
are no compatibility aliases, automatic CRD conversion, or supported Helm
in-place upgrades from the old identity. The API version remains v1alpha1.

The migration preserves the existing architecture and functional behavior of
resource discovery, selection, extraction, the restricted JSONPath subset,
typed values, operators, aggregations, authorization, admission validation,
reconciliation, status, limits, observability, and lifecycle. Admission,
observability, and lifecycle identifiers change only where the identity
requires it; validation decisions, metric semantics, and cleanup safety do
not change.

This specification supersedes the old public identity clauses in the existing
feature contracts, including `kubeseer-api-foundation`,
`installation-access-policy`, `admission-validation`, `observability`,
`packaging-and-installation`, `end-to-end-scenarios`,
`local-development-environment`, `local-cluster-resume`, and
`release-distribution`. Their behavioral requirements remain applicable.
Historical specifications and execution evidence remain records of work
performed under their original identity; they must not be silently rewritten
or presented as fresh KubeFacet certification.

<!-- assumed: this is one coordinated identity-only feature, with the existing
Kubernetes matrix and alpha version retained (source: maintainer migration
request, hack/toolchain.mk, charts/kubeseer/Chart.yaml). -->

The pre-edit identifier inventory is recorded in `identity-inventory.md`.

## Requirements

### R1 Identity-Only Behavioral Boundary

**User Story:** As a maintainer, I want a deliberate identity migration, so
that KubeFacet preserves the operator's existing behavior.

#### Acceptance Criteria

1. `R1.AC1` The system SHALL preserve resource discovery, resource selection, field extraction, and the supported restricted JSONPath semantics.
   - Acceptance check: existing discovery, selection, and extraction scenarios retain the same inputs and behavioral outcomes after identity translation.
2. `R1.AC2` The system SHALL preserve typed values, operators, and aggregation semantics.
   - Acceptance check: existing scalar, composite, filtering, arithmetic, grouping, and reducer scenarios retain their behavioral assertions.
3. `R1.AC3` The system SHALL preserve authorization and admission decisions apart from the renamed API identities.
   - Acceptance check: authorized and forbidden requests, fail-closed validation, RBAC separation, and runtime read boundaries retain their outcomes against the new APIs.
4. `R1.AC4` The system SHALL preserve reconciliation and status semantics.
   - Acceptance check: existing freshness, cancellation, conflict, invalidation, ordering, condition, and semantic status-write assertions pass unchanged in meaning.
5. `R1.AC5` The system SHALL preserve limits and observability behavior apart from renamed identifiers.
   - Acceptance check: limit outcomes, sanitized telemetry, metric types, labels, cardinality, buckets, and observation points match the baseline.
6. `R1.AC6` The system SHALL preserve installation, upgrade-within-identity, rollback-within-identity, uninstall, and purge lifecycle behavior apart from necessarily renamed identifiers.
   - Acceptance check: lifecycle scenarios retain ownership checks, exact destructive confirmation, unrelated-resource protection, and reinstall behavior under KubeFacet.

### R2 Kubernetes API And Public Go Types

**User Story:** As a resource author, I want a coherent Facet API, so that
the resource identity matches KubeFacet throughout Kubernetes and Go.

#### Acceptance Criteria

1. `R2.AC1` The system SHALL serve `Facet` at `kubefacet.steeltanuki.it/v1alpha1`.
   - Acceptance check: scheme registration and API-server discovery resolve the namespaced main resource as `facets.kubefacet.steeltanuki.it`.
2. `R2.AC2` The system SHALL serve `FacetAccessPolicy` at `kubefacet.steeltanuki.it/v1alpha1`.
   - Acceptance check: scheme registration and API-server discovery resolve the cluster-scoped policy resource as `facetaccesspolicies.kubefacet.steeltanuki.it`.
3. `R2.AC3` The system SHALL retain `installation-access-ceiling` as the canonical policy singleton name.
   - Acceptance check: policy admission, loading, bootstrap, and lifecycle checks target exactly that name under the new policy Kind.
4. `R2.AC4` The system SHALL expose consistently renamed public Go resource, list, spec, status, nested, helper, and validation identifiers.
   - Acceptance check: `Facet`, `FacetList`, `FacetSpec`, `FacetStatus`, and corresponding `FacetAccessPolicy` identifiers compile with all production consumers and tests; obsolete public aliases are absent.
5. `R2.AC5` The system SHALL register admission endpoints and webhook rules for the new API identities.
   - Acceptance check: rendered webhook paths, registration rules, typed validators, and real AdmissionReview tests agree on both new Kinds, plurals, group, and version.
6. `R2.AC6` The system SHALL preserve serialized spec and status contracts apart from API identity.
   - Acceptance check: generated schemas retain field names, defaulting, validations, subresources, scope, storage version, and structural constraints after normalizing identity-specific metadata and descriptions.
7. `R2.AC7` The system SHALL omit serving and conversion support for the obsolete API identities.
   - Acceptance check: no active scheme, CRD, webhook, API alias, or conversion webhook serves `kubeseer.io`, `Kubeseer`, or `KubeseerAccessPolicy`.

### R3 Module, Executables, And Source Paths

**User Story:** As a Go consumer, I want canonical KubeFacet module and
executable identities, so that builds and imports use the new project.

#### Acceptance Criteria

1. `R3.AC1` The system SHALL declare `github.com/steeltanuki/kubefacet` as its Go module.
   - Acceptance check: the module declaration and every internal import use the canonical path, with no replace directive or forwarding alias for the old module.
2. `R3.AC2` The system SHALL build the primary executable as `kubefacet` from `cmd/kubefacet`.
   - Acceptance check: canonical source and container builds produce and launch the renamed manager executable.
3. `R3.AC3` The system SHALL name its supporting executables and command directories `kubefacet-local` and `kubefacet-purge`.
   - Acceptance check: local harnesses, purge tooling, build targets, container commands, and documentation resolve the renamed command paths.
4. `R3.AC4` The system SHALL rename current source paths that encode the obsolete project or API identity.
   - Acceptance check: API source/test paths, project command paths, and current scripts use their new identities; unrelated implementation concepts keep their existing names.

### R4 Runtime-Visible Identity

**User Story:** As an operator administrator, I want runtime objects to use
one consistent identity, so that installation and diagnostics remain coherent.

#### Acceptance Criteria

1. `R4.AC1` The system SHALL use KubeFacet names for project-owned Deployments, Services, ServiceAccounts, webhook registrations, and certificate resources.
   - Acceptance check: default and customized Helm renders, manager lifecycle checks, and certificates reference matching new names and DNS SANs.
2. `R4.AC2` The system SHALL use `kubefacet.steeltanuki.it/` for project-owned label and annotation keys.
   - Acceptance check: rendered resources, ownership validation, cleanup, examples, and probes use the same new key domain.
3. `R4.AC3` The system SHALL use KubeFacet identity for its project-specific controller, leader-election, logger, Event reporter, and field-manager identifiers.
   - Acceptance check: controller setup, leases, Event components, log/trace names, and field-manager strings contain no operational old identity.
4. `R4.AC4` The system SHALL use selectors that match the renamed rendered workloads.
   - Acceptance check: readiness, EndpointSlice probes, lifecycle checks, E2E observation, and cleanup find the intended `app.kubernetes.io/name=kubefacet` resources.
5. `R4.AC5` The system SHALL use KubeFacet identity in CLI and diagnostic output.
   - Acceptance check: version, help, runtime errors, local diagnostics, and lifecycle messages use the appropriate project name or Facet Kind.

### R5 Project-Owned Environment Variables And Storage Roots

**User Story:** As an administrator or contributor, I want coherent settings
and state locations, so that old and new project environments are distinguishable.

#### Acceptance Criteria

1. `R5.AC1` The system SHALL name every project-owned environment variable with the `KUBEFACET_` prefix.
   - Acceptance check: runtime configuration, build/release metadata, package tests, local workflows, E2E, acceptance fault injection, and state/cache overrides agree on the new prefix.
2. `R5.AC2` The system SHALL omit deprecated `KUBESEER_` environment-variable aliases.
   - Acceptance check: no active environment lookup, exported harness setting, or documented current setting uses the obsolete prefix.
3. `R5.AC3` The system SHALL use `kubefacet` in project-owned state, cache, artifact, and temporary-directory names.
   - Acceptance check: defaults and isolated verification roots target the new identity without moving, deleting, or adopting old installations' state.

### R6 Metrics And Other Observability Identifiers

**User Story:** As an operator, I want telemetry to identify KubeFacet, so
that dashboards and diagnostics use the new project identity.

#### Acceptance Criteria

1. `R6.AC1` The system SHALL prefix every project-owned Prometheus metric with `kubefacet_`.
   - Acceptance check: metric registration, exposition, boundary checks, integration assertions, E2E probes, and current documentation agree on all renamed metrics.
2. `R6.AC2` The system SHALL omit duplicate or compatibility registrations under `kubeseer_`.
   - Acceptance check: the metric registry and rendered metrics endpoint expose no obsolete project-owned metric family.
3. `R6.AC3` The system SHALL rename project-specific trace instrumentation, span names, attributes, and telemetry correlation keys consistently.
   - Acceptance check: observability scenarios retain their correlation and confidentiality assertions using the new identity-specific keys.

### R7 Helm And Generated Packaging

**User Story:** As an installer, I want a canonical KubeFacet chart, so that
package contents, workload identity, and installation commands agree.

#### Acceptance Criteria

1. `R7.AC1` The system SHALL provide the Helm chart named `kubefacet` in `charts/kubefacet`.
   - Acceptance check: chart metadata, packaging, lint, rendering, helper namespaces, values schema, and chart documentation use the new identity.
2. `R7.AC2` The system SHALL use the chart description `Kubernetes operator for building typed, aggregated views of Kubernetes resources across namespaces`.
   - Acceptance check: `Chart.yaml` contains the exact description.
3. `R7.AC3` The system SHALL include chart keywords `kubernetes`, `operator`, `aggregation`, `custom-resources`, and `resource-views`.
   - Acceptance check: chart metadata contains all five concepts.
4. `R7.AC4` The system SHALL retain the current supported Kubernetes range and compatibility matrix.
   - Acceptance check: the chart retains `>=1.35.0-0 <1.37.0-0` and canonical verification retains Kubernetes `1.35.6` and `1.36.2` with the existing node-image mappings.
5. `R7.AC5` The system SHALL default to Helm release `kubefacet` and installation namespace `kubefacet-system`.
   - Acceptance check: current installation commands, local defaults, release fixtures, and default workload renders agree on those identities.
6. `R7.AC6` The system SHALL default the manager image repository to `ghcr.io/steeltanuki/kubefacet`.
   - Acceptance check: chart values, schema, rendered Deployments and hooks, container metadata, and package assertions agree on that repository.
7. `R7.AC7` The system SHALL derive generated deepcopy code and CRDs from the renamed API sources through the canonical generation workflow.
   - Acceptance check: clean generation reproduces the committed Go artifacts and both new-group CRDs, with no manually maintained obsolete generated CRD.
8. `R7.AC8` The system SHALL keep chart CRD copies and generated CRD checksum metadata synchronized with the generated sources.
   - Acceptance check: chart copies are byte-for-byte identical to generated CRDs and published checksum metadata matches those bytes.

### R8 Release And Distribution Readiness

**User Story:** As a release maintainer, I want future releases to publish
KubeFacet artifacts safely, so that the new identity starts at v0.2.0.

#### Acceptance Criteria

1. `R8.AC1` The system SHALL prepare current chart and application release metadata for `0.2.0`.
   - Acceptance check: chart `version` and `appVersion` are both `0.2.0`; current distribution checks accept a matching `v0.2.0` candidate.
2. `R8.AC2` The system SHALL address future manager images as `ghcr.io/steeltanuki/kubefacet:<version>`.
   - Acceptance check: release staging, OCI metadata, public consumer commands, and disposable-registry transaction assertions target the new image identity.
3. `R8.AC3` The system SHALL address future Helm OCI charts as `oci://ghcr.io/steeltanuki/charts/kubefacet`.
   - Acceptance check: release tooling, package metadata, consumer documentation, and disposable-registry assertions target that chart identity.
4. `R8.AC4` The system SHALL preserve release publication safety gates.
   - Acceptance check: ordinary CI, branches, develop, and PRs cannot publish; protected stable tags, exact gated source SHA, least permissions, immutable artifacts, retry/conflict handling, and fail-closed preflight retain their existing assertions.
5. `R8.AC5` The system SHALL leave historical v0.1.x releases and historical GHCR artifacts unchanged.
   - Acceptance check: this migration creates no public release or tag and performs no historical release/package mutation or deletion; local registry fixtures are explicitly disposable.

### R9 Local Development, Examples, And E2E

**User Story:** As a contributor, I want reproducible KubeFacet environments
and examples, so that the renamed operator can be exercised locally.

#### Acceptance Criteria

1. `R9.AC1` The system SHALL default the persistent kind cluster to `kubefacet-local` and its context to `kind-kubefacet-local`.
   - Acceptance check: toolchain declarations, owned-node validation, state files, diagnostics, readiness, resume, and cleanup agree on the new identities.
2. `R9.AC2` The system SHALL retain Podman as the container engine for local development and container-backed verification.
   - Acceptance check: container workflows use the existing Podman provider and preserve rejection of unsupported providers or unintended external clusters.
3. `R9.AC3` The system SHALL rename project-owned local and E2E namespaces, fixtures, sentinel values, state paths, and cleanup targets consistently.
   - Acceptance check: local acceptance tests and E2E harness acceptance prove ownership, isolation, selector agreement, and bounded cleanup under the new names.
4. `R9.AC4` The system SHALL provide current example manifests using `Facet` and the new API group.
   - Acceptance check: example resource manifests are named `facet.yaml`, and labels, namespaces, fixture CRDs, references, and selectors remain coherent.
5. `R9.AC5` The system SHALL preserve each example's functional meaning.
   - Acceptance check: all existing example verification scenarios produce their original typed, aggregated, degraded, and denied outcomes after identity translation.

### R10 Current Documentation And Breaking Migration Procedure

**User Story:** As an installer or resource author, I want accurate current
documentation and an explicit migration boundary, so that I can adopt KubeFacet.

#### Acceptance Criteria

1. `R10.AC1` The system SHALL use KubeFacet and `github.com/steeltanuki/kubefacet` throughout current user-facing documentation.
   - Acceptance check: README, CONTRIBUTING, API reference, installation, configuration, security, operations, troubleshooting, examples, development, Helm documentation, and current specifications use the new canonical identity.
2. `R10.AC2` The system SHALL retain the README positioning `Declarative, typed views and aggregations over Kubernetes resources.`
   - Acceptance check: the README describes authors defining a Facet and KubeFacet continuously evaluating the resources it selects.
3. `R10.AC3` The system SHALL document the intentionally breaking migration in `docs/migration-from-kubeseer.md`.
   - Acceptance check: the document identifies the v0.1.x to v0.2.0 boundary and explicitly maps both Kinds, API group, module, chart, image, release, environment, and metrics identities.
4. `R10.AC4` The system SHALL document that Helm in-place upgrade from Kubeseer 0.1.x to KubeFacet 0.2.x is unsupported.
   - Acceptance check: the procedure explicitly states that CRDs are not automatically converted and that old installations require deliberate old-identity uninstall/purge before a new installation.
5. `R10.AC5` The system SHALL reference a reproducible historical lifecycle procedure for removing old installations.
   - Acceptance check: migration guidance points to old-version documentation/tooling at an immutable historical tag, preserves its confirmation and ownership rules, and states that historical releases remain available.
6. `R10.AC6` The system SHALL document the manual post-merge actions.
   - Acceptance check: the handoff includes GitHub repository rename, local remote update, description/topics/social preview review, GHCR visibility review, later v0.2.0 publication, and later Artifact Hub registration.

### R11 Historical Integrity And Obsolete-Identifier Audit

**User Story:** As a maintainer, I want historical truth and a durable identity
gate, so that old names remain only where they intentionally explain history.

#### Acceptance Criteria

1. `R11.AC1` The system SHALL preserve historical Walden execution evidence and historical release records.
   - Acceptance check: baseline hashes for individually inventoried historical files remain unchanged; old evidence is not fabricated as new-identity execution.
2. `R11.AC2` The system SHALL supersede only the obsolete public identity clauses of surviving behavioral contracts.
   - Acceptance check: a current contract mapping identifies the older specifications, renamed identity clauses, and unchanged semantic requirements without rewriting the whole history.
3. `R11.AC3` The system SHALL update active constitution, current documentation, scripts, and verification contracts that would otherwise enforce obsolete identity.
   - Acceptance check: current checks require the new identities and do not use historical documents as authority for obsolete operational names.
4. `R11.AC4` WHEN the repository identifier audit encounters an obsolete operational identity, the system SHALL fail verification.
   - Acceptance check: injecting an old module, Kind, API group, environment prefix, metric, chart, label selector, runtime name, or newly added active Walden contract produces a failing audit.
5. `R11.AC5` WHEN an obsolete identifier is intentionally preserved, the system SHALL classify its occurrence with an explicit historical or migration reason.
   - Acceptance check: the final audit reports each matching file and line with its reviewed reason; historical exemptions are bounded by exact file identities and do not blanket-exclude `.walden`.
6. `R11.AC6` The system SHALL integrate the obsolete-identifier audit into canonical repository verification.
   - Acceptance check: `make verify` and normal CI run the durable gate, including case-sensitive, case-insensitive, and identity-bearing path checks.

### R12 Verification, Reviewable Commits, And Completion Honesty

**User Story:** As a reviewer, I want complete migration evidence and coherent
commits, so that I can assess readiness for the first KubeFacet release.

#### Acceptance Criteria

1. `R12.AC1` The system SHALL validate the new specification before changing implementation.
   - Acceptance check: requirements, design, tasks, verification coverage, and applicable review gates are recorded before implementation begins.
2. `R12.AC2` The system SHALL retain the original behavioral assertions in identity-dependent tests.
   - Acceptance check: test diffs change names and expected identities without removing coverage, weakening failure conditions, or replacing real collaborators with vacuous assertions.
3. `R12.AC3` The system SHALL pass all canonical verification required for a project-wide identity migration.
   - Acceptance check: `make verify`, `make test`, generated/API checks, envtest/admission/authorization, Helm/CRD consistency, local acceptance/resume checks, Kubernetes and package compatibility, E2E harness acceptance, full E2E certification, and all release-distribution scenarios succeed with the supported Podman workflows.
4. `R12.AC4` The system SHALL preserve logically reviewable local commits.
   - Acceptance check: the specification precedes API/runtime implementation, packaging/distribution changes, and documentation completion; commit boundaries contain related changes and preserve unrelated work.
5. `R12.AC5` IF canonical verification fails or an operational obsolete identifier remains, THEN the system SHALL report the migration as incomplete.
   - Acceptance check: the final report distinguishes executed passes, failures, and unrun checks and never claims completion with unresolved required evidence.
6. `R12.AC6` The system SHALL report the specification, major identity changes, generated artifacts, verification results, residue classifications, and manual post-merge actions.
   - Acceptance check: the handoff contains all six classes and states that the repository itself and public release publication remain maintainer actions.

## Non-Functional Requirements

- `NFR1` **Semantic stability:** preserve architecture, determinism, security decisions, and operational behavior; covered by `R1.AC1` through `R1.AC6` and `R12.AC2`.
- `NFR2` **Reproducibility:** regenerate artifacts from source and run non-vacuous, bounded, read-only verification against the supported toolchain; covered by `R7.AC7`, `R7.AC8`, and `R12.AC3`.
- `NFR3` **Historical integrity:** preserve old execution facts while distinguishing current identity contracts; covered by `R8.AC5` and `R11.AC1` through `R11.AC3`.
- `NFR4` **Isolation and safety:** preserve owned-cluster cleanup and release safeguards without touching historical installations or public artifacts; covered by `R1.AC6`, `R5.AC3`, `R8.AC4`, `R8.AC5`, `R9.AC2`, and `R9.AC3`.
- `NFR5` **Reviewability:** make identity choices and remaining old-name occurrences individually explainable; covered by `R11.AC5`, `R12.AC4`, and `R12.AC6`.

## Constraints And Dependencies

- `C1` The target identities are those explicitly requested by the maintainer; the API remains `v1alpha1` and the first new-identity release is `v0.2.0`.
- `C2` The current implementation and existing approved behavioral contracts are the semantic baseline. This feature supersedes identity only, not their functional requirements.
- `C3` Use the repository's canonical `make generate`, `make manifests`, and `make package-sync-crds` workflows and extend checksum generation where necessary; do not hand-patch generated CRDs.
- `C4` Preserve Kubernetes versions, dependency versions, supported architecture, container security, release policy, licensing, copyright, and optional contributor Walden usage.
- `C5` Use Podman-backed kind workflows and explicitly owned verification environments; never fall back to ambient kubeconfig, external clusters, Docker, or unrelated container state.
- `C6` Follow the repository's separate requirements, design, and tasks approvals; the maintainer's full execution request authorizes implementation after those gates are satisfied.
- `C7` Do not rename the hosted GitHub repository, change the local remote, tag or publish a release, mutate historical GHCR packages, register Artifact Hub, or push source commits as part of implementation.
- `C8` The existing clean `refactor/kubefacet-rename` branch is the implementation branch; the physical checkout path may retain its old name outside repository content.
- `C9` Preserve historical feature directory identifiers and recorded evidence; any current interpretation of an older contract must cite this identity supersession explicitly.

## Out Of Scope

- Compatibility aliases for old API groups, Kinds, Go public types, environment variables, metrics, charts, or runtime identities.
- Conversion webhooks, automatic manifest conversion, dual API serving, or in-place old-identity Helm upgrades.
- Discovery, selection, extraction grammar, value semantics, operators, aggregations, authorization, reconciliation, status, admission decisions, limits, or telemetry behavior changes.
- Unrelated refactoring, dependency or supported-Kubernetes changes, new architectures, new packaging formats, and new local environment providers.
- Retirement/deletion of historical Walden specifications, rewriting evidence, backdating reviews, or presenting old evidence as current certification.
- Hosting account actions, release publication, global Podman cleanup, automatic removal of old installations, and remote changes.
