# Pre-Migration Project Identity Inventory

Baseline commit: `a09dc37581dbbe632d28022c384cf90521d5929d`.

This is migration documentation, not an obsolete-identifier exemption for
active implementation. It records the old checkout before edits and describes
which categories require different treatment. Historical hashes are recorded
in `historical-identity-records.json`; generated outputs are regenerated rather
than edited. Files created later are not covered by this inventory.

The case-sensitive variants are `Kubeseer`, `kubeseer`, `KUBESEER`, and
`kubeseer.io`. The case-insensitive scan also identifies other casing and
identity-bearing paths. Git metadata, the physical checkout directory, and
external pre-existing installations are outside source-content migration.

| Category | Files | Matching lines | Treatment |
| --- | ---: | ---: | --- |
| Active Walden context | 1 | 20 | Rename intentionally by category; update coupled consumers and behavioral expectations. |
| Build, release, local harnesses, verification | 34 | 450 | Rename intentionally by category; update coupled consumers and behavioral expectations. |
| Current documentation and configuration | 15 | 356 | Rename intentionally by category; update coupled consumers and behavioral expectations. |
| Current examples and fixtures | 18 | 80 | Rename intentionally by category; update coupled consumers and behavioral expectations. |
| Existing Walden contracts: historical identity, surviving semantics | 66 | 1101 | Pre-migration approved specification; this feature supersedes identity clauses only. Preserve approved bytes and review bindings; current semantic verification uses renamed canonical checks. |
| Generated CRDs | 2 | 70 | Rename intentionally by category; update coupled consumers and behavioral expectations. |
| Helm metadata, templates, values, documentation, CRD copies | 28 | 374 | Rename intentionally by category; update coupled consumers and behavioral expectations. |
| Historical public release records | 5 | 21 | Published v0.1.x history and reproducibility references; preserve bytes and links. |
| Historical workflow lessons | 1 | 6 | Dated observations of old-identity work; preserve historical facts. |
| Integration, envtest, E2E, fixtures, certification contract | 74 | 1483 | Rename intentionally by category; update coupled consumers and behavioral expectations. |
| Production source, command directories, package tests | 70 | 752 | Rename intentionally by category; update coupled consumers and behavioral expectations. |
| Public Go API, API tests, generated deepcopy | 6 | 494 | Rename intentionally by category; update coupled consumers and behavioral expectations. |
| Recorded historical Walden evidence | 21 | 217 | Actual pre-migration execution under the old identity; preserve bytes and provenance. |

## Coupled Identity Decisions

- Brand `Kubeseer` becomes `KubeFacet`; main API Kind and Go type become `Facet`. These are distinct mappings.
- Policy Kind and public Go type `KubeseerAccessPolicy` become `FacetAccessPolicy`; singleton `installation-access-ceiling` remains.
- API/owned-label domain `kubeseer.io` becomes `kubefacet.steeltanuki.it`; resource plurals become `facets` and `facetaccesspolicies`.
- Existing admission paths encode both the old API domain and Kinds; source registration, TLS/lifecycle probes, Helm rules, and admission fixtures must change together.
- Main/helper commands, module imports, chart helpers, image labels, ownership identities, state roots, environment settings, metrics, and trace keys require separate mappings.
- The nine current metric families retain their metric types, bounded labels, buckets, and observation points.
- Local and E2E selectors must agree with Helm `app.kubernetes.io/name=kubefacet`, including EndpointSlice readiness and cleanup.
- Chart and application metadata advance from `0.1.6` to `0.2.0`; disposable release fixtures using `v0.1.3` must become new-identity fixture versions without rewriting historical releases.
- Kubernetes range stays `>=1.35.0-0 <1.37.0-0`; API compatibility stays `1.35.6` and `1.36.2`; existing pinned dependencies and node images remain.
- `SPECIFICATIONS.md`, the constitution, and current scripts must reference the identity supersession while historical feature directory IDs remain intact.
- `test/e2e/certification.json` is an active certification contract, not immutable execution evidence.
- `docs/release-pipeline-audit.md` contains current release guidance mixed with historical findings; preserve dated facts and rewrite active instructions deliberately.
- `.walden/lessons.md` records dated historical events; do not rewrite old quotations or executed-command identities.

## File-Level Inventory

Each entry lists all matching baseline line numbers. This explains the scope
before mutation; the final operational audit must find no active residue.

The historical manifest also binds existing specification/evidence files that
contain no obsolete identifier: 98 files in total, including the 93 matching
historical files in the table. This protects historical records independently
of whether their contents need an identifier exemption.

### Active Walden context

- `.walden/constitution.md`: 1, 3, 7, 12, 18, 21, 23, 35, 36, 43, 44, 52, 53, 71, 115, 118, 127, 140, 142, 143.

### Build, release, local harnesses, verification

- `.github/workflows/ci.yml`: 55, 57, 71, 82.
- `.github/workflows/release.yml`: 11, 126.
- `Dockerfile`: 14, 22, 23, 27, 30, 34.
- `Makefile`: 33, 67, 71.
- `go.mod`: 1.
- `hack/apply-compatible-crds.sh`: 28, 29.
- `hack/check-crd-compatibility.sh`: 73, 74.
- `hack/e2e-harness-acceptance.sh`: 48, 74, 148, 157, 160, 170, 195, 204, 216, 223, 224, 232, 287, 290, 296, 347, 353, 354, 356, 357, 371, 385, 393, 395, 400, 404, 418, 425.
- `hack/e2e-harness.sh`: 28, 29, 32, 202, 203, 211, 212, 227, 229, 244, 255, 272, 278, 341, 348, 377, 386, 471, 477, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527.
- `hack/envtest-assets.sh`: 37, 45.
- `hack/envtest-harness-acceptance.sh`: 45, 97.
- `hack/local-environment-acceptance.sh`: 19, 46, 47, 48, 55, 196, 221, 233, 237, 295, 383, 400, 413, 433, 440, 451, 498, 521.
- `hack/local-environment.sh`: 25, 26, 27, 28, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 135, 136, 137, 138, 266, 475, 485, 490, 533, 563, 592, 599, 632, 633, 634, 731, 750, 762, 773, 774, 775, 788, 823, 826, 858.
- `hack/local-examples.sh`: 22, 24, 25, 26, 27, 45, 46, 65, 66, 67, 68, 69, 70, 71, 83, 91, 92, 126, 135, 136, 140, 141, 147, 151, 153, 158, 170, 181, 189.
- `hack/package-cluster-smoke.sh`: 52, 53, 54, 55, 56, 57, 60, 90, 99, 103, 104, 105, 110, 113, 114, 115, 116, 123, 124, 125, 126, 132, 133, 134, 141, 142.
- `hack/package-sync-crds.sh`: 13, 16.
- `hack/release-distribution-http.py`: 57, 268.
- `hack/release-distribution.sh`: 12, 215, 218, 229, 250, 277, 283, 285, 286, 287, 294, 297, 298, 300, 308, 313, 320, 323, 329, 363, 365, 400, 401, 409, 414, 477, 486, 487, 496, 498, 516, 519, 532, 539, 541, 542, 549, 550, 563, 575, 599, 600, 602, 604, 609, 610, 633, 634, 635, 636, 652, 653, 662, 693, 709, 720, 757, 778, 783, 790, 808, 822, 847, 877, 878, 882, 883, 884.
- `hack/test-layer-policy-acceptance.sh`: 40, 81, 91, 100, 110, 118, 119.
- `hack/test-local-cluster-resume.sh`: 14, 16, 18, 76, 77, 157.
- `hack/test-local-environment.sh`: 13, 28, 90.
- `hack/test-package-compatibility.sh`: 13, 14, 31, 54, 56, 57, 67, 68.
- `hack/test-release-distribution.sh`: 15, 51, 58, 60, 63, 76, 160, 162, 164, 177, 178, 188, 189, 210, 243, 245, 265, 289, 295, 313, 336, 349, 357, 366, 367, 410, 413, 425, 432, 434, 464, 465, 474, 475, 476, 563, 605, 611, 648, 674, 676, 719, 728, 749, 771, 785, 786, 794, 795, 796, 802, 809, 832, 833, 835, 838, 839, 845, 846, 849, 850, 853, 911, 916, 917, 930, 931, 1041, 1042.
- `hack/toolchain.mk`: 35, 36, 37, 38.
- `hack/uninstall-kubeseer.sh`: 23, 31.
- `hack/verify-admission-boundaries.sh`: 77.
- `hack/verify-e2e-boundaries.sh`: 60, 86, 88.
- `hack/verify-generated.sh`: 55, 56, 58, 59.
- `hack/verify-local-environment.sh`: 46, 48, 50, 59, 62, 96, 97, 111, 119, 127, 152, 162, 163, 168, 169, 170, 171, 175, 181, 191, 224, 227.
- `hack/verify-observability-boundaries.sh`: 88, 89, 90, 91, 92, 93, 94, 95, 96.
- `hack/verify-package.sh`: 13, 14, 42, 43, 54, 55, 69, 73, 91, 108, 114, 115, 119, 120, 125, 128, 131, 135, 140, 143, 171, 195, 200, 201, 202, 210, 212, 213, 214, 215, 216, 233, 235, 236, 237, 243, 246, 247, 248.
- `hack/verify-performance-and-limits-boundaries.sh`: 84.
- `hack/verify-release-workflows.go`: 181.
- `hack/verify-test-layer-policy.sh`: 18, 59, 68.

### Current documentation and configuration

- `CONTRIBUTING.md`: 1, 36, 37, 45, 118.
- `README.md`: 1, 5, 7, 12, 17, 22, 28, 30, 39, 40, 64, 68, 70, 87, 91, 94, 96, 100, 112, 120, 123, 124, 128, 138, 182, 183, 210, 212, 226, 235, 246, 258, 263, 280, 285.
- `SPECIFICATIONS.md`: 1, 5, 20, 27, 31, 39, 41, 53, 70, 95, 99, 126, 147, 177, 188, 210, 239, 240, 263, 265, 269, 278, 557, 561, 563, 577, 581, 593, 661, 677, 706, 711, 745, 762, 777, 799, 800, 838, 839, 861, 871, 888, 906, 910, 921, 932, 940, 949, 950, 974, 986, 996, 1008, 1028, 1032, 1083, 1092, 1093, 1115.
- `config/local/values.yaml`: 24, 25, 26, 27, 28, 29, 30, 31, 45, 54, 58, 62, 66, 70, 74, 75, 78, 82, 86, 90, 91, 97, 98, 99, 100, 101, 102, 103, 104.
- `docs/api-reference.md`: 3, 5, 7, 13, 16, 17, 43, 288, 289, 333, 334, 337, 343, 344.
- `docs/concepts-and-architecture.md`: 3, 9, 15, 29, 43, 48, 54, 79, 93, 134, 153, 196, 238.
- `docs/configuration.md`: 3, 6, 15, 44, 45, 46, 54, 114, 200, 225, 226, 227, 230.
- `docs/development.md`: 3, 35, 36, 37, 40, 78, 108, 109, 164.
- `docs/examples.md`: 3, 30, 52, 69, 71, 72, 73, 104.
- `docs/installation.md`: 1, 3, 4, 5, 24, 41, 45, 47, 52, 54, 61, 62, 63, 81, 82, 83, 84, 103, 104, 105, 130, 144, 165, 210, 211, 212, 213, 225, 235, 236, 237, 238, 259, 261, 280, 290, 292, 297, 312, 314, 324, 330, 332, 335, 343, 344, 346, 351, 354, 358, 376, 377, 378, 379, 380, 381, 382, 387.
- `docs/local-development.md`: 15, 16, 18, 20, 21, 45, 46, 61, 78, 79, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 118, 129, 130, 161.
- `docs/operations.md`: 25, 26, 27, 28, 29, 31, 32, 41, 42, 48, 54, 56, 77, 90, 108, 126, 128, 130, 131, 158, 165, 178, 179, 180, 181, 182, 183, 184, 185, 186, 209, 210, 223, 241, 244.
- `docs/release-pipeline-audit.md`: 22, 23, 24, 25, 26, 27, 141, 142.
- `docs/security.md`: 3, 13, 17, 29, 45, 94, 99, 101, 104, 110, 132, 156, 169, 216, 218, 219, 226.
- `docs/troubleshooting.md`: 7, 9, 10, 11, 22, 23, 24, 25, 33, 34, 48, 71, 94, 105, 108, 111, 129, 162, 180, 187, 216, 223, 225, 226, 238, 247, 248, 271, 272.

### Current examples and fixtures

- `examples/authorization-denial/kubeseer.yaml`: 3, 4, 7, 8, 13.
- `examples/authorization-denial/workload.yaml`: 7, 8.
- `examples/builtin-resource/README.md`: 10.
- `examples/builtin-resource/kubeseer.yaml`: 3, 4, 7, 9, 17.
- `examples/builtin-resource/workload.yaml`: 7, 9, 10, 15, 19, 20.
- `examples/cross-namespace-aggregation/kubeseer.yaml`: 3, 4, 7, 8, 13.
- `examples/cross-namespace-aggregation/workload.yaml`: 7, 8, 13, 20, 21, 26.
- `examples/custom-resource/fixture-crd.yaml`: 6, 7, 9.
- `examples/custom-resource/kubeseer.yaml`: 3, 4, 7, 8, 12, 13.
- `examples/custom-resource/workload.yaml`: 3, 7, 8.
- `examples/partial-degradation/fixture-crd.yaml`: 6, 7, 9.
- `examples/partial-degradation/kubeseer.yaml`: 3, 4, 7, 8, 13, 17, 18.
- `examples/partial-degradation/workload.yaml`: 7, 8, 13, 16, 20, 21.
- `examples/typed-extraction/README.md`: 8.
- `examples/typed-extraction/kubeseer.yaml`: 3, 4, 7, 8, 13.
- `examples/typed-extraction/workload.yaml`: 7, 9, 10, 14, 18, 19.
- `examples/value-operator/kubeseer.yaml`: 3, 4, 7, 8, 13.
- `examples/value-operator/workload.yaml`: 7, 9, 10, 13, 16.

### Existing Walden contracts: historical identity, surviving semantics

- `.walden/specs/admission-validation/design.md`: 22, 23, 69, 71, 206, 207, 210, 223, 254, 255, 260, 261, 289, 313, 321, 403, 476, 477, 478.
- `.walden/specs/admission-validation/requirements.md`: 13, 17, 29, 32, 34, 38, 48, 49, 50, 51, 52, 54, 58, 72, 81, 83, 89, 90, 94, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 115, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 140, 145, 147, 148, 160, 163, 164, 165, 168, 169, 170, 171, 176, 201, 206, 207, 220, 224, 225, 228, 237, 240.
- `.walden/specs/admission-validation/tasks.md`: 19, 40, 44, 76, 82, 104, 106, 113, 114, 137, 167, 195, 199, 224, 228, 232, 236, 239.
- `.walden/specs/authorization-enforcement/design.md`: 30, 47, 180, 356, 570, 668.
- `.walden/specs/authorization-enforcement/requirements.md`: 13, 23, 30, 32, 42, 46, 56, 61, 63, 73, 108, 118, 127, 128, 129, 139, 145, 151, 167, 176, 181, 186, 189, 193.
- `.walden/specs/authorization-enforcement/tasks.md`: 32, 56, 78, 105, 124, 145, 162, 166, 170, 174, 177.
- `.walden/specs/configuration-budget-status-invalidation/design.md`: 26, 101.
- `.walden/specs/configuration-budget-status-invalidation/requirements.md`: 13, 24, 51, 57, 68, 70, 98, 113.
- `.walden/specs/configuration-budget-status-invalidation/tasks.md`: 51, 63, 77, 81, 94.
- `.walden/specs/cross-namespace-aggregation/design.md`: 44, 97, 130, 132, 137, 141, 183, 185, 215, 216, 304, 321, 322, 325, 327, 329, 330, 331, 332, 335, 336, 337, 338, 341, 342, 343, 344, 347, 348, 349, 356, 358.
- `.walden/specs/cross-namespace-aggregation/requirements.md`: 39, 43, 55, 89, 110, 147, 168, 254.
- `.walden/specs/cross-namespace-aggregation/tasks.md`: 15, 24, 36, 67, 96, 120, 144, 175, 210, 214, 235, 239, 243, 247, 250.
- `.walden/specs/end-to-end-scenarios/design.md`: 33, 42, 121, 129, 220, 287, 294, 330, 359, 367, 385, 394, 451, 504, 511, 574.
- `.walden/specs/end-to-end-scenarios/requirements.md`: 13, 34, 95, 98, 99, 100, 101, 102, 109, 113, 119, 120, 130, 148, 169, 171, 191, 196, 197, 198, 199, 200, 240, 263, 266, 272, 276.
- `.walden/specs/end-to-end-scenarios/tasks.md`: 74, 99, 126, 141, 142, 145, 152.
- `.walden/specs/field-extraction/design.md`: 29, 96, 97, 125, 141, 172, 227, 248.
- `.walden/specs/field-extraction/requirements.md`: 13, 17, 26, 30, 34, 35, 38, 42, 107, 134, 135.
- `.walden/specs/field-extraction/tasks.md`: 15, 16, 20, 30, 51, 73, 95, 116, 119, 123, 127, 129.
- `.walden/specs/installation-access-policy/design.md`: 15, 16, 19, 41, 92, 94, 110, 123, 126, 127, 128, 136, 149, 172, 277, 369.
- `.walden/specs/installation-access-policy/requirements.md`: 14, 24, 33, 37, 38, 39, 40, 91, 102, 103, 104, 110, 142, 143, 147, 154.
- `.walden/specs/installation-access-policy/tasks.md`: 21, 22, 24, 26, 28, 29, 43, 44, 46, 48, 49, 73, 94, 111, 114, 117, 121, 123.
- `.walden/specs/integration-testing-foundation/design.md`: 15, 24, 123, 285, 473.
- `.walden/specs/integration-testing-foundation/requirements.md`: 14, 60, 166.
- `.walden/specs/integration-testing-foundation/tasks.md`: 41, 49, 52, 62, 71, 72, 80, 106, 108, 116, 120, 123, 127, 131, 133.
- `.walden/specs/kubeseer-api-foundation/design.md`: 11, 17, 21, 35, 74, 90, 91, 100, 121, 129, 134, 137, 138, 141, 144, 153, 154, 157, 167, 170, 173, 180, 181, 203, 220, 237, 262.
- `.walden/specs/kubeseer-api-foundation/requirements.md`: 13, 17, 18, 19, 26, 30, 31, 32, 33, 34, 35, 39, 43, 48, 49, 79, 83, 84, 96, 97, 110, 111, 124.
- `.walden/specs/kubeseer-api-foundation/tasks.md`: 15, 20, 21, 29, 30, 38, 47, 48, 56.
- `.walden/specs/local-cluster-resume/design.md`: 61, 108, 126.
- `.walden/specs/local-cluster-resume/tasks.md`: 74, 75.
- `.walden/specs/local-development-environment/design.md`: 23, 24, 34, 36, 40, 54, 79, 85, 115, 125, 127, 267, 297, 298, 299, 322, 325, 376, 377, 394, 395, 399, 400, 403, 446, 447, 507, 544.
- `.walden/specs/local-development-environment/requirements.md`: 13, 33, 87, 90, 94, 95, 108, 116, 127, 128, 139, 144, 151, 152, 169, 178, 181, 213, 229, 234, 246, 252, 253, 257, 262, 281, 285, 309, 315, 323, 326.
- `.walden/specs/local-development-environment/tasks.md`: 54, 92, 109, 128, 136, 190, 201, 220, 263, 300, 304, 350.
- `.walden/specs/native-scalar-conversion-compatibility/design.md`: 211.
- `.walden/specs/native-scalar-conversion-compatibility/requirements.md`: 14, 18, 19, 40, 57, 90, 117.
- `.walden/specs/native-scalar-conversion-compatibility/tasks.md`: 50, 62, 76, 80, 94.
- `.walden/specs/observability/design.md`: 80, 162, 238, 270, 273, 279, 293, 294, 295, 296, 297, 298, 299, 300, 301, 314, 357, 360.
- `.walden/specs/observability/requirements.md`: 13, 34, 47, 48, 55, 88, 89, 90, 91, 92, 93, 94, 95, 96, 99, 105, 106, 107, 108, 109, 110, 111, 112, 113, 116, 123, 133, 191, 192, 206, 215, 219, 226, 228, 233, 240.
- `.walden/specs/observability/tasks.md`: 14, 40, 66, 93, 122, 126, 150, 165, 177, 181, 190, 200, 204, 208, 212, 215.
- `.walden/specs/packaging-and-installation/design.md`: 15, 16, 19, 24, 36, 45, 46, 61, 80, 101, 103, 112, 137, 139, 140, 142, 143, 158, 170, 182, 256, 271, 333, 335, 340, 364, 475.
- `.walden/specs/packaging-and-installation/requirements.md`: 13, 23, 28, 29, 45, 53, 64, 74, 81, 98, 131, 136, 137, 138, 147, 160, 161, 162, 172, 173, 174, 177, 178, 188, 217, 218, 262, 288, 289, 294, 295, 309, 324, 333, 334, 350, 355, 357, 367, 368, 370, 378, 380, 388, 391, 392.
- `.walden/specs/packaging-and-installation/tasks.md`: 15, 31, 38, 74, 116, 137, 161, 185, 197, 199, 211.
- `.walden/specs/performance-and-limits/design.md`: 129, 131, 144, 152, 207, 261, 320, 415, 419, 453.
- `.walden/specs/performance-and-limits/requirements.md`: 13, 21, 23, 28, 31, 38, 49, 51, 62, 73, 74, 75, 78, 87, 119, 133, 160, 161, 165, 167, 168, 183, 217, 218, 224, 229, 233, 237.
- `.walden/specs/performance-and-limits/tasks.md`: 33, 40, 44, 46, 56, 80, 106, 136, 140, 163, 173, 192, 196, 225, 229, 249, 253, 257, 261, 264.
- `.walden/specs/reconciliation-runtime/design.md`: 18, 23, 26, 36, 40, 46, 50, 60, 98, 104, 114, 133, 153, 176, 185, 209, 263, 351, 370, 397, 423, 444, 470, 526, 584.
- `.walden/specs/reconciliation-runtime/requirements.md`: 15, 33, 34, 39, 41, 45, 46, 47, 48, 49, 50, 51, 52, 56, 62, 63, 64, 65, 66, 67, 69, 79, 80, 81, 84, 85, 89, 93, 94, 95, 96, 101, 102, 108, 123, 132, 142, 143, 144, 153, 154, 156, 157, 161, 168, 172, 173, 174, 175, 177, 184, 186, 190, 191, 196, 197, 211, 217.
- `.walden/specs/reconciliation-runtime/tasks.md`: 17, 19, 36, 38, 69, 78, 105, 134, 141, 150, 156, 158, 180, 202, 221, 224, 228, 232, 234.
- `.walden/specs/release-distribution/design.md`: 105, 106, 107, 126, 131, 171, 172, 197, 198.
- `.walden/specs/release-distribution/requirements.md`: 16, 81, 82, 119, 120, 141, 148, 165, 279.
- `.walden/specs/resource-discovery/design.md`: 23, 292.
- `.walden/specs/resource-discovery/requirements.md`: 13, 22, 38, 97, 104.
- `.walden/specs/resource-discovery/tasks.md`: 18, 27, 36, 46, 55, 65, 74.
- `.walden/specs/resource-selection/design.md`: 17, 29, 92, 93, 102, 146, 170.
- `.walden/specs/resource-selection/requirements.md`: 13, 18, 27, 35, 36, 42, 46, 52, 53, 57, 98, 133, 134, 137.
- `.walden/specs/resource-selection/tasks.md`: 15, 20, 30, 51, 70, 93, 97, 118, 122, 142, 162, 165, 169, 173, 175.
- `.walden/specs/status-and-conditions/design.md`: 15, 51, 96, 147, 151, 154, 156, 159, 240, 271, 342, 345, 363, 543.
- `.walden/specs/status-and-conditions/requirements.md`: 13, 17, 32, 39, 44, 45, 51, 52, 53, 55, 60, 79, 87, 108, 109, 117, 129, 130, 131, 171, 241, 243, 248, 249, 250, 261.
- `.walden/specs/status-and-conditions/tasks.md`: 15, 16, 20, 30, 57, 88, 119, 145, 166, 187, 208, 211, 215, 219, 221.
- `.walden/specs/typed-output-model/design.md`: 19, 40, 57, 109, 134, 135, 140, 147, 148, 150, 160, 215, 228, 230, 246, 249, 250, 251, 252, 253, 254, 255, 256, 257, 260, 263, 266, 267, 270, 272, 273, 274, 275, 278, 284, 287, 289, 290, 291, 292, 295, 296, 302, 303, 308, 313, 318, 324, 330, 331, 400, 411.
- `.walden/specs/typed-output-model/requirements.md`: 13, 26, 30, 36, 40, 70, 134, 180, 181.
- `.walden/specs/typed-output-model/tasks.md`: 15, 17, 21, 31, 58, 82, 90, 107, 133, 153, 156, 160, 164, 166.
- `.walden/specs/value-operators/design.md`: 47, 67, 93, 156, 157, 199, 200, 254, 259, 276, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 297, 300, 301, 304, 305, 306, 307, 310, 311, 323, 329, 330, 350.
- `.walden/specs/value-operators/requirements.md`: 14, 39, 43, 53, 78, 101, 125, 147, 192, 221.
- `.walden/specs/value-operators/tasks.md`: 15, 16, 20, 32, 61, 85, 107, 138, 173, 177, 197, 201, 205, 209, 212.
- `.walden/specs/watch-startup-cancellation/requirements.md`: 54.
- `.walden/specs/watch-startup-cancellation/tasks.md`: 53, 65, 79, 83, 97.

### Generated CRDs

- `config/crd/bases/kubeseer.io_kubeseeraccesspolicies.yaml`: 7, 9, 11, 12, 13, 14, 20, 41, 42.
- `config/crd/bases/kubeseer.io_kubeseers.yaml`: 7, 9, 11, 12, 13, 14, 20, 41, 47, 53, 62, 93, 114, 123, 127, 149, 170, 186, 207, 264, 352, 420, 425, 430, 434, 447, 451, 462, 494, 509, 514, 541, 548, 563, 570, 593, 605, 628, 634, 639, 667, 674, 697, 709, 731, 739, 764, 780, 792, 812, 818, 830, 834, 847, 854, 877, 889, 908, 917, 957, 975.

### Helm metadata, templates, values, documentation, CRD copies

- `charts/kubeseer/Chart.yaml`: 2, 3, 8, 10, 12, 13, 15, 16.
- `charts/kubeseer/README.md`: 1, 4, 17, 25, 26, 27, 28, 51, 64, 67, 107, 121, 138, 139, 140, 141, 150.
- `charts/kubeseer/crds/kubeseer.io_kubeseeraccesspolicies.yaml`: 7, 9, 11, 12, 13, 14, 20, 41, 42.
- `charts/kubeseer/crds/kubeseer.io_kubeseers.yaml`: 7, 9, 11, 12, 13, 14, 20, 41, 47, 53, 62, 93, 114, 123, 127, 149, 170, 186, 207, 264, 352, 420, 425, 430, 434, 447, 451, 462, 494, 509, 514, 541, 548, 563, 570, 593, 605, 628, 634, 639, 667, 674, 697, 709, 731, 739, 764, 780, 792, 812, 818, 830, 834, 847, 854, 877, 889, 908, 917, 957, 975.
- `charts/kubeseer/templates/_helpers.tpl`: 11, 15, 19, 28, 32, 36, 37, 38, 41, 43, 44, 47, 48, 52, 55, 58, 59, 62, 63, 66, 67, 70, 74, 78, 79, 82, 83, 86, 87, 90, 91, 94, 95, 96, 99.
- `charts/kubeseer/templates/deployment.yaml`: 4, 5, 7, 9, 21, 25, 27, 41, 43, 53, 55, 56, 73, 122, 127, 133.
- `charts/kubeseer/templates/lifecycle-hook-rbac.yaml`: 1, 2, 6, 7, 19, 31, 32, 44, 55, 58, 59, 64, 65, 77, 99, 110, 113, 114.
- `charts/kubeseer/templates/metrics-service.yaml`: 5, 6, 8, 10, 14.
- `charts/kubeseer/templates/package-identity-configmap.yaml`: 4, 5, 7, 9, 13, 14.
- `charts/kubeseer/templates/policy-bootstrap-configmap.yaml`: 8, 12, 13, 15, 17.
- `charts/kubeseer/templates/policy-hook-job.yaml`: 5, 6, 8, 10, 20, 22, 33, 35, 39, 53, 58.
- `charts/kubeseer/templates/policy-hook-rbac.yaml`: 5, 6, 8, 10, 18, 20, 22, 27, 28, 34, 36, 38, 45, 48, 49.
- `charts/kubeseer/templates/post-delete-hook-job.yaml`: 4, 5, 7, 9, 19, 21, 32, 34.
- `charts/kubeseer/templates/pre-delete-hook-job.yaml`: 4, 5, 7, 9, 19, 21, 32, 34.
- `charts/kubeseer/templates/preflight-hook-job.yaml`: 4, 5, 7, 9, 19, 21, 32, 34, 40, 41, 44.
- `charts/kubeseer/templates/rbac-authors.yaml`: 6, 9, 11, 13, 14, 16, 17, 24, 27, 29, 33.
- `charts/kubeseer/templates/rbac-observed-cluster.yaml`: 5, 7, 9, 23, 25, 27, 31, 34, 35.
- `charts/kubeseer/templates/rbac-observed-namespaced.yaml`: 6, 9, 11, 23, 26, 28, 32, 35, 36.
- `charts/kubeseer/templates/rbac-operator.yaml`: 7, 9, 11, 13, 14, 16, 17, 19, 20, 35, 37, 39, 43, 46, 47.
- `charts/kubeseer/templates/serviceaccount.yaml`: 4, 5, 7, 9.
- `charts/kubeseer/templates/uninstall-hook-rbac.yaml`: 1, 2, 6, 7, 19, 35, 46, 49, 50, 55, 56, 68, 80, 81, 87, 98, 101, 102.
- `charts/kubeseer/templates/validating-webhook-configuration.yaml`: 4, 6, 8, 10, 13, 20, 21, 23, 29, 31, 32, 39, 40, 42, 48, 50.
- `charts/kubeseer/templates/verify-hook-job.yaml`: 4, 5, 7, 9, 19, 21, 32, 34, 40, 41, 44, 45, 51, 72, 77, 83.
- `charts/kubeseer/templates/webhook-ca-configmap.yaml`: 5, 6, 8, 10.
- `charts/kubeseer/templates/webhook-certificate.yaml`: 2, 7, 8, 10, 12, 19, 20, 22, 24, 27, 28, 32, 39, 40, 42, 44, 47, 53, 54, 56, 58, 60, 66, 67, 68, 69.
- `charts/kubeseer/templates/webhook-service.yaml`: 4, 5, 7, 9, 14.
- `charts/kubeseer/values.schema.json`: 219, 221.
- `charts/kubeseer/values.yaml`: 1, 7, 30, 33, 96, 110.

### Historical public release records

- `docs/releases/v0.1.0.md`: 1, 5, 7, 13, 16.
- `docs/releases/v0.1.1.md`: 1, 5, 7, 12, 14.
- `docs/releases/v0.1.3.md`: 1, 7, 11, 14.
- `docs/releases/v0.1.4.md`: 1, 7, 11, 14.
- `docs/releases/v0.1.6.md`: 1, 8, 12.

### Historical workflow lessons

- `.walden/lessons.md`: 8, 12, 16, 20, 238, 278.

### Integration, envtest, E2E, fixtures, certification contract

- `test/e2e/assertions.go`: 23, 41, 48, 55, 70, 84, 130.
- `test/e2e/certification.json`: 3, 21, 39, 63.
- `test/e2e/data_pipeline_scenarios.go`: 23, 47, 51, 96, 100, 125, 133, 134, 137, 169, 171, 187, 242, 244, 252.
- `test/e2e/fixtures.go`: 40, 73, 74, 103, 279, 280, 282, 285, 289, 293, 294.
- `test/e2e/fixtures/forbidden-sentinels.txt`: 3.
- `test/e2e/fixtures/widget-crd.yaml`: 18, 20.
- `test/e2e/lifecycle_scenarios.go`: 48, 50, 74, 87, 99, 122, 124, 159, 161, 188, 202, 204, 207, 208, 210, 211, 217, 238, 240, 242, 244, 248, 250, 277, 296, 342, 369.
- `test/e2e/negative_scenarios.go`: 23, 48, 53, 86, 88, 99, 103, 124, 126, 141, 143.
- `test/e2e/observability_scenario.go`: 41, 42, 44, 51, 58, 84, 105.
- `test/e2e/observer.go`: 26, 41, 43, 49, 50, 153, 156, 165, 197, 218, 228, 238.
- `test/e2e/scenarios.go`: 85, 91, 98, 101.
- `test/e2e/session.go`: 32, 49, 50, 55, 56, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 114, 216, 257, 258, 259, 265, 267, 269, 276, 305, 307, 309, 312, 313, 314, 318, 319, 331.
- `test/e2e/values.yaml`: 25, 39, 51, 68.
- `test/envtest/admission_validation_envtest_test.go`: 28, 29, 30, 31, 32, 63, 92, 105, 108, 116, 173, 178, 179, 186, 193, 195, 197, 198, 201, 203, 205, 206, 209, 215, 219, 225, 229, 239, 250, 251, 253, 287, 289, 292, 300, 320, 322, 323, 325, 339, 350, 352, 364, 366, 371, 373, 380, 382, 394, 401, 407, 453, 454, 455, 459, 473, 474, 475, 480.
- `test/envtest/harness.go`: 409, 567.
- `test/envtest/reconciliation_runtime_envtest_test.go`: 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 126, 180, 181, 182, 185, 192, 244, 255, 263, 265, 268, 273, 279, 300, 301, 303, 306, 342, 364, 366, 369, 377, 379, 382, 393, 395, 398, 402, 416, 417, 419, 424, 426, 442, 443, 447, 450, 453, 457, 503, 527, 543, 560, 570, 639, 641, 649, 652, 668, 670, 676, 679, 687, 701, 739, 741, 747, 750, 760, 762, 765, 774, 776, 778, 782, 788, 790, 799, 813, 816, 823, 862, 864, 867, 878, 879, 896, 935, 951, 967, 969, 971, 973, 975, 977, 979, 995, 1010, 1013, 1041, 1062, 1114, 1129, 1136, 1144, 1158, 1184, 1224, 1239, 1247, 1259, 1270, 1272, 1277, 1282, 1287, 1292, 1315, 1316, 1318, 1322, 1323, 1330, 1333, 1337, 1338, 1344, 1364, 1367, 1369, 1371, 1375, 1376, 1381, 1386, 1394, 1395, 1400, 1420, 1421, 1424, 1425, 1428, 1431, 1459, 1462, 1484, 1514, 1515, 1517, 1521, 1528, 1564, 1575, 1576, 1578, 1580, 1619, 1681, 1880, 1885, 1893, 1916, 1919, 1943, 1947, 1966, 1979, 1989, 1992, 1997, 2004, 2020, 2045, 2047, 2050, 2095, 2097, 2100, 2120, 2134, 2147, 2161, 2173, 2180, 2182, 2184, 2186, 2189, 2235, 2237, 2245, 2257, 2259, 2277, 2285, 2287, 2296, 2352, 2360, 2363, 2372, 2374, 2376, 2378, 2382, 2415, 2445, 2478, 2509, 2557, 2561, 2619, 2627, 2770, 2793, 2814, 2818.
- `test/integration/authorization_enforcement_core_test.go`: 25, 26, 27, 28, 131, 134.
- `test/integration/authorization_enforcement_list_test.go`: 24, 25, 26, 27, 28, 37.
- `test/integration/authorization_enforcement_pipeline_test.go`: 27, 28, 29, 30, 31, 32, 33, 56, 151, 174, 221, 237, 238, 240, 266, 292, 329, 330, 334, 399, 404, 420.
- `test/integration/authorization_enforcement_watch_test.go`: 26, 27, 28, 29, 30, 39, 57, 58, 124, 173.
- `test/integration/configuration_budget_documentation_test.go`: 23, 24, 175, 184.
- `test/integration/configuration_budget_status_test.go`: 26, 27, 28, 29, 30, 31, 113, 149, 151, 157, 197, 198, 201, 202.
- `test/integration/cross_namespace_aggregation_arithmetic_test.go`: 22, 23, 24, 30, 32, 38, 83, 85, 91, 127, 129, 135.
- `test/integration/cross_namespace_aggregation_grouping_test.go`: 22, 23, 24, 30, 32, 33, 38, 119, 121, 127.
- `test/integration/cross_namespace_aggregation_isolation_test.go`: 23, 24, 25, 26, 27, 28, 42, 53, 55, 59, 78, 89, 104, 105, 121, 159, 169, 178, 182.
- `test/integration/cross_namespace_aggregation_pipeline_test.go`: 22, 23, 24, 34, 38, 42, 48, 52, 54, 55.
- `test/integration/cross_namespace_aggregation_planning_test.go`: 22, 23, 24, 25, 26, 31, 42, 45, 99, 126, 133, 157.
- `test/integration/cross_namespace_aggregation_reducers_test.go`: 21, 22, 23, 31, 47, 49, 50, 55, 60, 61, 108, 110, 111, 152, 162.
- `test/integration/cross_namespace_aggregation_status_test.go`: 23, 24, 25, 26, 33, 35, 39, 92, 95, 111, 114, 116, 124, 126, 148.
- `test/integration/field_extraction_batch_test.go`: 25, 26, 27, 36, 37, 38, 51, 65, 67, 72, 84, 85, 100, 101, 120, 121, 122.
- `test/integration/field_extraction_native_values_test.go`: 24, 25, 26, 102, 104, 158, 172, 191, 193.
- `test/integration/field_extraction_planning_test.go`: 21, 22, 45, 47, 81, 83, 117, 119, 133, 136, 141, 142, 159, 161.
- `test/integration/installation_access_policy_test.go`: 30, 31, 32, 33, 34, 35, 374, 416, 503, 508, 509, 510, 513, 516, 517, 520, 523, 526, 543, 560, 561, 569, 574, 576, 577, 588, 589, 601, 602, 604, 613, 615, 617, 619, 626, 628, 631, 633, 634, 641, 644, 646, 653, 655, 659, 660, 667, 673, 680, 686, 693, 699, 707, 708, 715, 722, 735, 748, 761, 779, 780, 781, 783, 785, 787, 788, 791, 792, 793, 794, 811, 813, 816, 819, 835, 840, 845, 848, 853, 857, 901, 904, 907, 912, 913, 916, 923, 940, 948, 949, 952, 955, 965, 987, 994, 1019, 1020, 1022, 1028, 1029, 1063, 1081, 1096, 1109, 1116, 1119, 1132, 1143, 1158, 1178, 1182, 1193, 1196, 1203, 1209, 1227, 1228, 1238, 1253, 1263, 1265, 1276, 1279, 1306, 1307, 1308, 1313, 1319, 1321, 1328, 1422, 1427, 1435, 1436, 1446, 1454, 1455, 1459, 1467, 1469, 1472, 1477, 1483, 1484, 1489, 1491, 1494, 1501, 1506, 1518, 1521, 1522, 1543, 1580, 1590, 1604, 1615, 1624, 1632, 1642, 1663, 1685, 1722, 1731, 1737, 1738, 1740, 1747, 1797.
- `test/integration/local_environment_endpointslice_test.go`: 23, 34, 35, 74, 89, 107.
- `test/integration/native_scalar_documentation_test.go`: 12, 13, 14, 15, 90, 127, 140, 142.
- `test/integration/native_scalar_pipeline_test.go`: 10, 11, 12, 13, 14, 15, 22, 24, 146, 181, 183, 184, 185, 191, 220, 236, 238, 239, 240, 259.
- `test/integration/observability_boundaries_test.go`: 25, 26, 27, 28, 29, 30, 45, 92, 93.
- `test/integration/observability_core_test.go`: 28, 29, 71, 95, 132, 150, 151, 152, 153, 154, 155, 156, 157, 158.
- `test/integration/observability_manager_test.go`: 29, 30, 31, 32, 33, 34, 35, 71, 101, 194, 195, 196, 197, 198, 199, 200, 264, 271, 296.
- `test/integration/observability_runtime_test.go`: 26, 27, 28, 29, 30, 31, 32, 55, 72, 73, 74, 81, 94, 130, 144, 145, 159, 173, 178.
- `test/integration/observability_status_test.go`: 24, 25, 26, 27, 63, 88, 139, 143, 171, 196, 197.
- `test/integration/observability_watch_test.go`: 25, 26, 27, 28, 29, 38, 55, 92, 106, 160.
- `test/integration/packaging_manager_image_test.go`: 22, 23, 24, 38, 39, 41, 42, 49.
- `test/integration/packaging_policy_test.go`: 31, 32, 43, 44, 61.
- `test/integration/packaging_rbac_test.go`: 31, 34, 47, 48, 67, 80, 88, 92.
- `test/integration/packaging_uninstall_purge_test.go`: 24, 34, 37, 38, 66, 70, 79.
- `test/integration/packaging_upgrade_rollback_test.go`: 21, 42, 43, 60.
- `test/integration/packaging_webhook_tls_test.go`: 33, 48, 49, 51, 52, 73, 74, 94, 175, 176, 177, 178, 287, 292.
- `test/integration/packaging_workload_test.go`: 34, 35, 45, 67, 73.
- `test/integration/performance_limits_profile_test.go`: 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 65, 79, 100, 107, 114, 124, 166, 187, 192, 200, 214, 255, 301, 304, 305, 388, 396, 397, 398, 399, 400, 401, 418, 458, 491, 495, 496, 499, 523, 532, 590, 664, 710, 728, 770, 798, 1216, 1217, 1218, 1227.
- `test/integration/reconciliation_runtime_pipeline_test.go`: 26, 27, 28, 29, 30, 31, 32, 33, 46, 50, 52, 56, 58, 62, 65, 143, 148, 172, 200, 228, 230, 243, 257, 298, 299, 301, 367, 368, 375, 433, 451, 488, 489, 493, 500, 501, 517, 545, 548, 549, 556, 561, 567, 577, 578, 583, 588, 607, 728.
- `test/integration/reconciliation_runtime_status_test.go`: 25, 26, 27, 42, 43, 47, 53, 55, 56, 57, 58, 60, 61, 62, 65, 68, 69, 71, 154, 181, 185, 197, 209, 222, 256, 260, 262, 266, 271, 272, 278, 280, 281, 284, 286, 288, 289, 293, 305, 309, 313, 323, 332, 336, 350.
- `test/integration/reconciliation_runtime_test.go`: 23, 24, 39, 40, 55, 62, 63, 75, 78, 91, 97, 100, 149, 153, 154, 184, 190, 191, 198, 204, 210, 230, 231.
- `test/integration/reconciliation_runtime_watch_test.go`: 27, 28, 29, 30, 31, 32, 52, 61, 86, 103, 130, 188, 192, 244, 313, 352.
- `test/integration/resource_selection_authorization_test.go`: 22, 23, 24, 25, 26, 33.
- `test/integration/resource_selection_execution_test.go`: 23, 24, 25, 26, 38, 111.
- `test/integration/resource_selection_failures_test.go`: 23, 24, 25, 35, 56, 84, 102, 110, 117, 126, 127, 128, 161.
- `test/integration/resource_selection_pagination_test.go`: 24, 25, 26, 78, 197.
- `test/integration/resource_selection_planning_test.go`: 24, 25, 26, 35, 80, 81, 99, 111, 112, 139, 159.
- `test/integration/status_conditions_conditions_test.go`: 23, 24, 33, 60, 70, 77, 103, 132, 150, 161, 165, 172.
- `test/integration/status_conditions_pipeline_test.go`: 23, 24, 25, 26, 27, 28, 44, 48, 50, 75, 80, 85, 118, 124, 128, 150, 159, 160, 165, 186, 187, 203, 205, 224, 225, 250.
- `test/integration/status_conditions_publisher_test.go`: 22, 23, 24, 38, 39, 55, 57, 58, 61, 65, 117, 182, 194, 203, 216.
- `test/integration/status_conditions_result_test.go`: 25, 26, 34, 38, 42, 48, 52, 69, 77, 104, 107, 112, 120, 121, 122, 123, 124, 127, 145, 146, 153.
- `test/integration/typed_output_cardinality_test.go`: 22, 23, 24, 25, 31, 33.
- `test/integration/typed_output_conversions_test.go`: 27, 28, 29, 30, 38, 40, 43, 100, 116, 154, 207, 209, 216, 405, 407, 409.
- `test/integration/typed_output_isolation_test.go`: 23, 24, 25, 26, 32, 34, 39, 86, 89, 104, 120, 128, 152, 153, 154, 155.
- `test/integration/typed_output_serialization_test.go`: 25, 26, 27, 28, 35, 37, 99, 151, 163, 175, 183, 200, 232, 236, 239.
- `test/integration/value_operators_comparisons_test.go`: 22, 23, 24, 25, 26, 35, 37, 50, 55, 57, 64, 66, 73, 76, 80, 85, 94, 96, 98, 100, 102, 107, 115.
- `test/integration/value_operators_isolation_test.go`: 23, 24, 25, 26, 27, 34, 35, 42, 49, 56, 65, 66, 77, 81.
- `test/integration/value_operators_planning_test.go`: 22, 23, 24, 25, 26, 32, 34, 37, 39, 45, 46, 47, 49, 51, 52, 53, 54, 55, 58, 98, 100, 102, 131, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 148, 161, 162, 163, 206, 207, 210, 214, 215, 218, 219, 222, 223, 226, 230, 231, 234, 235, 238, 239, 242, 243, 246, 248.
- `test/integration/value_operators_predicates_test.go`: 20, 21, 30, 42, 46, 56, 66, 70, 72, 74, 79, 81, 83, 85, 87, 89.
- `test/integration/value_operators_transformations_test.go`: 22, 23, 24, 25, 26, 27, 35, 42, 49, 55, 67, 75, 83, 93, 94, 95, 102, 136, 137, 140.
- `test/integration/watch_startup_cancellation_test.go`: 27, 28, 29, 30, 31, 32, 65, 119, 153, 155, 160, 165, 171, 194, 242, 311, 312, 405, 415, 418, 485, 553, 626, 627, 698, 769, 825, 878, 978, 1030, 1091, 1239, 1252, 1273.
- `test/integration/watch_startup_documentation_test.go`: 9, 60, 112.

### Production source, command directories, package tests

- `cmd/kubeseer-local/main.go`: 20, 92, 104.
- `cmd/kubeseer-purge/main.go`: 26, 44, 48, 59, 73.
- `cmd/kubeseer/main.go`: 28, 29, 30, 142, 165, 166, 212, 213, 217, 237, 274, 275.
- `internal/accesspolicy/compiler.go`: 22, 62, 105, 120, 124.
- `internal/accesspolicy/doc.go`: 16.
- `internal/accesspolicy/evaluator.go`: 20.
- `internal/accesspolicy/loader.go`: 21, 30, 35, 37, 52, 53, 58, 76.
- `internal/admission/budgets.go`: 16, 30, 31, 35, 55, 69, 83, 97, 138, 139, 141, 143, 148, 155, 157, 158, 161, 164, 170, 197, 202, 208, 228, 229, 270, 271.
- `internal/admission/semantic.go`: 22, 23, 24, 25, 26, 27, 36, 39, 63, 74, 90, 110, 131, 223, 224, 253, 262, 271.
- `internal/admission/validator.go`: 22, 23, 24, 25, 26, 66, 69, 73, 77, 130, 131, 140, 215.
- `internal/admission/webhook.go`: 24, 34, 35, 37, 39, 41, 42, 43, 53, 54, 57, 58, 59, 60, 63, 64, 65, 66, 69, 73, 77, 81, 85, 87, 89, 96, 100, 104, 108, 110, 112, 176, 177, 178, 187, 188, 242, 243.
- `internal/aggregation/contracts.go`: 30, 31, 32, 33, 34, 91, 121, 140, 188, 195, 201, 203, 207, 218, 224, 239, 343, 352, 376, 377, 382, 385, 443, 445, 455, 461.
- `internal/aggregation/evaluator.go`: 20, 21, 22, 23.
- `internal/aggregation/grouping.go`: 21, 22, 23.
- `internal/aggregation/keys.go`: 21, 22.
- `internal/aggregation/planner.go`: 20, 21, 29, 32, 49, 81, 92, 170, 187, 199, 209.
- `internal/aggregation/reducers.go`: 21, 22, 23.
- `internal/aggregation/result.go`: 20, 21, 22, 23, 33, 41, 43, 52, 55, 64, 71, 72, 83, 84, 98, 102, 109, 113, 121, 122, 125, 129, 131, 141, 146, 151, 152, 160, 164, 168, 170, 175, 178, 182, 184, 190, 194, 205, 207, 209, 218, 222.
- `internal/authorization/contracts.go`: 22, 23, 27.
- `internal/authorization/enforcer.go`: 20.
- `internal/discovery/contracts.go`: 26.
- `internal/discovery/envtest_test.go`: 27, 99, 100, 107, 108, 128, 129, 175, 178, 180.
- `internal/extraction/batch.go`: 20, 21, 22, 28, 56.
- `internal/extraction/compiler.go`: 22, 30, 40, 42, 96, 103.
- `internal/extraction/contracts.go`: 21.
- `internal/extraction/doc.go`: 16.
- `internal/extraction/evaluator.go`: 22.
- `internal/extraction/outcomes.go`: 17.
- `internal/limits/profile.go`: 48, 74, 88, 140, 154, 211, 225, 321, 363, 449.
- `internal/localprobe/probe.go`: 17, 63, 67, 68, 69, 70, 181, 405, 428, 446, 455, 461, 515, 535, 552, 598, 630, 660, 926, 947, 966, 1063, 1064, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1128.
- `internal/managerapp/application.go`: 36, 37, 38, 39, 40, 41, 56, 59, 60, 61, 100, 101, 102, 103, 290.
- `internal/managerapp/cleanup.go`: 23, 113, 123.
- `internal/managerapp/lifecycle.go`: 26, 45, 46, 47, 48, 49, 63, 95, 96, 147, 173, 272, 374, 375.
- `internal/managerapp/policy.go`: 19, 49, 72.
- `internal/managerapp/version.go`: 28.
- `internal/observability/metrics.go`: 38, 39, 40, 41, 42, 43, 44, 45, 46, 56, 60, 72, 76.
- `internal/observability/observer.go`: 28, 29, 208, 209, 210, 211, 212, 291, 292, 432, 433, 456, 457, 458, 459, 521, 522, 523, 524, 659, 661, 670.
- `internal/observability/vocabulary.go`: 20, 21.
- `internal/operators/contracts.go`: 31, 32, 33, 144, 155, 190, 201.
- `internal/operators/evaluator.go`: 21, 22, 23, 24, 138, 307, 357.
- `internal/operators/planner.go`: 24, 25, 31, 33, 116, 127, 181, 241, 285, 301, 316, 327, 337, 351.
- `internal/operators/status.go`: 20, 21, 27, 28, 32, 35, 39, 41, 49, 51, 54, 56, 71, 76, 80, 85, 93, 99.
- `internal/purge/purge.go`: 19, 47, 48, 49, 54, 56, 58, 62, 64.
- `internal/reconciliation/contracts.go`: 23, 24, 25, 26, 27, 28, 29, 30, 44, 91, 93, 94, 97, 98, 99, 102, 104, 105, 106, 109, 111, 131, 132, 146, 160, 182, 185, 259, 275, 276, 281, 282, 284, 288, 289, 290, 293, 294, 296, 299, 304, 306, 308, 311, 327, 329, 332.
- `internal/reconciliation/doc.go`: 15.
- `internal/reconciliation/errors.go`: 21, 78.
- `internal/reconciliation/events.go`: 21, 40, 42, 44, 48, 52, 56, 57, 60, 78, 97, 110, 111, 124, 138, 152, 156, 160, 164, 175, 183, 190, 207, 211, 218, 222, 226, 227.
- `internal/reconciliation/pipeline.go`: 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 41, 75, 85, 115, 118, 134, 159, 467, 497, 498, 501, 557, 584, 627, 691, 736, 758, 837.
- `internal/reconciliation/routes.go`: 24, 25, 26, 27, 28.
- `internal/reconciliation/setup.go`: 21, 22, 23, 24, 25, 26, 27, 28, 29, 39, 97, 141, 143, 145, 149.
- `internal/reconciliation/status.go`: 22, 23, 24, 25, 36, 38, 44, 45, 60, 66, 76, 107, 117, 146, 151, 240, 242, 246, 250, 256, 260, 264.
- `internal/reconciliation/tracker.go`: 22, 23, 82, 177.
- `internal/reconciliation/trigger.go`: 25, 26, 35, 63, 94, 330, 332, 360, 362.
- `internal/selection/binder.go`: 18, 19.
- `internal/selection/contracts.go`: 21, 22.
- `internal/selection/envtest_test.go`: 23, 24, 25, 26, 27, 28, 58, 98, 116, 131, 146, 159, 170, 182, 184, 188, 194, 209, 235, 237, 239, 273, 281.
- `internal/selection/executor.go`: 22, 23, 24.
- `internal/selection/planner.go`: 22, 23, 48, 91, 104.
- `internal/status/conditions.go`: 22, 100, 111, 113, 116, 120, 126, 133, 135, 300, 309, 465.
- `internal/status/doc.go`: 16.
- `internal/status/result.go`: 24, 31, 32, 40, 64, 127, 132, 159, 160, 191.
- `internal/typedoutput/aggregation_bridge.go`: 27, 33, 90, 118, 132, 160, 164, 189, 231.
- `internal/typedoutput/batch.go`: 20, 21, 27, 45.
- `internal/typedoutput/contracts.go`: 21, 22, 115, 125.
- `internal/typedoutput/converters.go`: 27, 28, 90, 153, 205, 299, 402.
- `internal/typedoutput/operator_bridge.go`: 23, 24, 31, 37, 175, 181, 187.
- `internal/typedoutput/outcomes.go`: 22, 23, 24, 25, 51, 61, 322, 326, 334.
- `internal/typedoutput/planner.go`: 20, 26, 28, 63, 73.
- `internal/typedoutput/status.go`: 26, 27, 28, 34, 35, 39, 43, 50, 52, 56, 58, 65, 70, 73, 75, 83, 87, 95, 97, 99, 107, 111, 119, 121, 124, 126, 130, 134, 136, 140, 146, 150, 155, 157, 162, 164, 167, 169, 173, 179, 185, 188, 194, 200, 206, 208, 214, 217, 219, 225, 229, 234, 238, 242, 246, 332, 338, 342, 346, 348.
- `internal/typedoutput/value.go`: 20, 39, 68, 77.

### Public Go API, API tests, generated deepcopy

- `api/v1alpha1/doc.go`: 15, 17, 25.
- `api/v1alpha1/groupversion_info.go`: 23, 31, 32, 33, 34.
- `api/v1alpha1/kubeseer_access_policy_types.go`: 36, 39, 41, 45, 48, 51, 54, 57, 58.
- `api/v1alpha1/kubeseer_envtest_test.go`: 27, 28, 29, 46, 47, 48, 49, 50, 56, 59, 95, 99, 102, 104, 113, 143, 146, 147, 162, 164, 173, 174, 177, 178, 184, 198, 199, 200, 201, 206, 216, 222, 228, 230, 232, 247, 252, 259, 264, 278, 281, 295, 305, 308, 311, 313, 315, 352, 386, 405, 417, 442, 464, 536, 565, 586, 655, 678, 690, 702, 715, 718, 735, 744, 745, 749, 753, 759, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 780, 783, 788, 789, 792, 794, 797, 798, 799, 805, 806, 807, 814, 820, 823, 828, 845, 857, 858, 859, 860, 861, 862, 865, 871, 872, 873, 875, 876, 877, 883, 888, 905, 915, 947, 949, 958, 967, 968, 973, 991, 1014, 1042, 1066, 1083, 1084, 1088, 1122, 1129, 1448, 1635, 1637, 1640, 1643, 1650, 1657, 1667, 1674, 1698, 1704, 1710, 1720, 1730, 1740, 1750, 1760, 1770, 1793, 1802, 1856, 1970, 1971, 1973, 2047, 2058, 2310, 2324, 2328, 2355, 2358.
- `api/v1alpha1/kubeseer_types.go`: 22, 25, 28, 33, 34, 37, 40, 43, 46, 47, 52, 55, 57, 66, 78, 84, 87, 89, 92, 93, 94, 95, 96, 97, 98, 99, 100, 103, 105, 108, 109, 110, 111, 114, 117, 124, 145, 148, 150, 165, 170, 173, 176, 179, 180, 181, 182, 183, 184, 185, 186, 187, 190, 192, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 213, 214, 216, 219, 224, 227, 231, 233, 306, 307, 318, 326, 329, 330, 341, 343, 346, 349, 351, 354, 355, 358, 360, 363, 364, 365, 368, 370, 373, 374, 377, 378, 383, 387, 391, 395, 398, 401, 403, 406, 407, 408, 411, 414, 417, 418, 421, 422, 427, 433, 437, 441, 444, 447, 448, 453, 456, 459, 460, 463, 466, 470, 473, 474, 476, 479, 483, 486, 488, 490, 494, 497, 498, 515, 517, 519, 522, 525, 527, 545, 548, 551, 552, 557, 560, 564, 567, 570, 572, 574, 592, 595, 604, 606, 614, 616, 624, 625, 636, 637.
- `api/v1alpha1/zz_generated.deepcopy.go`: 29, 37, 38, 42, 48, 56, 63, 64, 68, 74, 82, 88, 95, 96, 100, 106, 114, 126, 127, 131, 137, 141, 149, 154, 155, 159, 165, 170, 171, 175, 181, 186, 191, 192, 196, 202, 208, 209, 213, 219, 223, 230, 235, 240, 241, 245, 251, 255, 262, 263, 267, 273, 287, 288, 292, 298, 302, 303, 307, 313, 317, 324, 325, 329, 335, 339, 340, 344, 350, 354, 361, 366, 367, 371, 377, 383, 390, 391, 395, 401, 409, 413, 418, 425, 426, 430, 436, 485, 486, 490, 496, 500, 501, 505, 511, 515, 516, 520, 526, 530, 537, 542, 543, 547, 553, 557, 564, 565, 569, 575, 579, 580, 584, 590, 605, 612, 619, 620, 624, 630, 634, 639, 646, 653, 658, 659, 663, 669, 673, 680, 681, 685, 691, 702, 707, 712, 713, 717, 723, 727, 728, 732, 738, 766, 771, 786, 787, 791.

### Recorded historical Walden evidence

- `.walden/evidence/admission-validation.json`: 33, 43, 81, 119, 157, 195, 233, 243, 281, 291, 301, 311, 321.
- `.walden/evidence/authorization-enforcement.json`: 33, 71, 109, 147, 185, 223, 261, 271, 281, 291, 301.
- `.walden/evidence/configuration-budget-status-invalidation.json`: 32, 33, 79, 80, 127, 128, 142, 143, 189, 190.
- `.walden/evidence/cross-namespace-aggregation.json`: 33, 71, 109, 147, 185, 223, 261, 271, 309, 319, 329, 339, 349.
- `.walden/evidence/end-to-end-scenarios.json`: 69, 107, 145, 183.
- `.walden/evidence/field-extraction.json`: 33, 71, 109, 147, 185, 195, 205, 215, 225.
- `.walden/evidence/installation-access-policy.json`: 33, 71, 109, 147, 185, 195, 205, 215, 225.
- `.walden/evidence/integration-testing-foundation.json`: 79, 117, 127, 165, 203, 241, 332, 342, 380, 390, 400, 410, 420, 430.
- `.walden/evidence/kubeseer-api-foundation.json`: 3, 33, 71, 109, 147, 185.
- `.walden/evidence/local-development-environment.json`: 78, 88, 171, 301, 394, 441.
- `.walden/evidence/native-scalar-conversion-compatibility.json`: 32, 33, 79, 80, 126, 127, 145, 146, 188, 189.
- `.walden/evidence/observability.json`: 33, 71, 109, 147, 157, 195, 233, 243, 281, 291, 301, 311, 321.
- `.walden/evidence/packaging-and-installation.json`: 33, 154, 229, 267, 305, 343, 381.
- `.walden/evidence/performance-and-limits.json`: 33, 71, 109, 147, 185, 195, 233, 271, 281, 319, 329, 367, 377, 387, 397, 407.
- `.walden/evidence/reconciliation-runtime.json`: 33, 71, 109, 147, 185, 223, 261, 299, 309, 319, 329, 339.
- `.walden/evidence/resource-discovery.json`: 33, 71, 109, 147, 185, 223, 261.
- `.walden/evidence/resource-selection.json`: 33, 71, 109, 147, 157, 195, 205, 243, 281, 291, 301, 311, 321.
- `.walden/evidence/status-and-conditions.json`: 33, 71, 109, 147, 185, 223, 261, 299, 309, 319, 329, 339.
- `.walden/evidence/typed-output-model.json`: 33, 71, 109, 147, 185, 223, 233, 243, 253, 263.
- `.walden/evidence/value-operators.json`: 33, 71, 109, 147, 185, 223, 233, 271, 281, 291, 301, 311.
- `.walden/evidence/watch-startup-cancellation.json`: 32, 33, 80, 81, 128, 129, 148, 149, 191, 192.
