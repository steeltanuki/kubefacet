# Current KubeFacet Identity Contract

This file is the current identity overlay for the historical feature contracts
listed below. The approved [`project-identity-rename`](specs/project-identity-rename/requirements.md)
specification supersedes only their project, API, packaging, telemetry,
environment, and local-resource identity clauses. Their behavioral
requirements remain in force after translating resource identity to `Facet`
and `FacetAccessPolicy` in `kubefacet.steeltanuki.it/v1alpha1`.

Feature directory names and their approved documents remain historical
records. Do not rename or rewrite them to make the new product identity appear
retroactively. Their earlier execution evidence records work performed under
the original identity and is not current KubeFacet certification. The
`project-identity-rename` evidence is selected-feature evidence for this
migration only.

| Historical feature ID | Identity clauses superseded here | Behavioral contract that remains applicable |
| --- | --- | --- |
| [`kubeseer-api-foundation`](specs/kubeseer-api-foundation/requirements.md) | API group, resource Kinds, public Go type names, and generated-resource names | Serialized fields and meanings, namespace/scope rules, structural validation, defaults, status shape, and API-server behavior |
| [`installation-access-policy`](specs/installation-access-policy/requirements.md) | Policy Kind and API group | `installation-access-ceiling` singleton, deny-by-default policy semantics, scope limits, and separation from Kubernetes RBAC |
| [`admission-validation`](specs/admission-validation/requirements.md) | API group, Kinds, webhook paths, rules, and validator type names | Admission decisions, defaulting, validation limits, fail-closed behavior, and parity with runtime validation |
| [`observability`](specs/observability/requirements.md) | Metric, logger, Event, trace, span, and correlation prefixes that identify the project | Metric types, label meanings, cardinality, buckets, observation points, sanitization, and tracing semantics |
| [`packaging-and-installation`](specs/packaging-and-installation/requirements.md) | Chart, image, workload, executable, environment, and current install identities | Supported Kubernetes and Helm matrix, ownership, RBAC boundaries, certificate behavior, compatible same-identity upgrade/rollback, uninstall, and explicit-purge safeguards |
| [`end-to-end-scenarios`](specs/end-to-end-scenarios/requirements.md) | API fixtures, manager selectors, and release image/chart identities | The same product scenarios, real API checks, authorization boundaries, status semantics, telemetry assertions, isolation, and cleanup guarantees |
| [`local-development-environment`](specs/local-development-environment/requirements.md) | Project-owned cluster/context, release, namespace, state/cache paths, examples, and selectors | Podman-backed local workflow, ownership checks, resumability, bounded cleanup, and example outcomes |
| [`local-cluster-resume`](specs/local-cluster-resume/requirements.md) | Default cluster and context names used by project-owned recovery | Resume only a validated exited owned control plane; preserve its data, reject ambiguous or running-unreachable nodes, and avoid unrelated state |
| [`release-distribution`](specs/release-distribution/requirements.md) | Future v0.2.0 image/chart destinations and KubeFacet identity metadata | Protected-tag source binding, fail-closed preflight, immutable artifacts, retry/conflict handling, no publication from ordinary CI, and no mutation of historical releases |

The renamed regression interfaces and the evidence boundary are declared in
the approved migration tasks. Do not rewrite older evidence, rerun obsolete
one-time bootstrap or publication proofs, or describe this selected-feature
result as a verdict for the full historical portfolio.
