# Migration from Kubeseer v0.1.x to KubeFacet v0.2.0

KubeFacet v0.2.0 intentionally starts a new project and Kubernetes API
identity. This is a breaking migration. The KubeFacet package does not serve
the old API group, convert stored resources, provide compatibility aliases,
or support an in-place Helm upgrade from Kubeseer v0.1.x. A Helm upgrade
across this boundary is unsupported.
There is no CRD conversion webhook; stored resources remain under their old
API group and are not converted automatically.

## Identity mapping

| v0.1.x identity | v0.2.0 identity |
| --- | --- |
| `Kubeseer` namespaced custom resource | `Facet` namespaced custom resource |
| `KubeseerAccessPolicy` cluster-scoped custom resource | `FacetAccessPolicy` cluster-scoped custom resource |
| `kubeseer.io/v1alpha1` | `kubefacet.steeltanuki.it/v1alpha1` |
| `github.com/steeltanuki/kubeseer` | `github.com/steeltanuki/kubefacet` |
| chart `kubeseer` | chart `kubefacet` |
| image `ghcr.io/steeltanuki/kubeseer` | image `ghcr.io/steeltanuki/kubefacet` |
| Helm release `kubeseer` and namespace `kubeseer-system` | Helm release `kubefacet` and namespace `kubefacet-system` |
| project-owned `KUBESEER_` environment settings | project-owned `KUBEFACET_` settings; there are no old-prefix aliases |
| project-owned `kubeseer_` Prometheus metrics | project-owned `kubefacet_` metrics |
| old release tags and artifacts through v0.1.6 | future KubeFacet v0.2.0 tag and matching image/chart destinations |

The API version remains `v1alpha1`; existing field names and meanings remain
the same. The policy singleton remains named `installation-access-ceiling`,
but its Kind and API group change as shown above.

## Remove the old installation before installing KubeFacet

Helm cannot upgrade the v0.1.x release in place. The two operators use
different API groups and resource Kinds, and KubeFacet contains no CRD
conversion webhook. Existing custom resources are not converted or moved.
Export any values you need, plan how to recreate those declarations as
`Facet` and `FacetAccessPolicy`, and deliberately remove the old installation
before installing the new chart into a clean target.

Use the immutable v0.1.6 lifecycle instructions and matching old-version
tooling. The old normal uninstall removes its release-owned runtime objects
while retaining the old CRDs and custom resources. Its separately confirmed
purge deletes old custom-resource data and CRDs; follow that tool's exact
ownership checks and destructive confirmation procedure when removal is
intended:

- [v0.1.6 installation, uninstall, and purge procedure](https://github.com/steeltanuki/kubeseer/blob/v0.1.6/docs/installation.md#safe-uninstall-and-explicit-purge)
- [v0.1.6 `uninstall-kubeseer.sh` wrapper](https://github.com/steeltanuki/kubeseer/blob/v0.1.6/hack/uninstall-kubeseer.sh)

Do not use the KubeFacet purge executable for the old API group. After the old
release has been deliberately removed and the desired old data has been
exported, install KubeFacet v0.2.0 as a new release using the
[installation guide](installation.md). Historical v0.1.x releases remain
available for their original lifecycle procedure.

## Maintainer actions after merge

The repository identity migration does not change hosting or publish artifacts.
After the change is reviewed and merged, the maintainer must:

1. Rename the GitHub repository to `steeltanuki/kubefacet`.
2. Update the maintainer's local Git remote to the renamed repository.
3. Review the GitHub description, topics, and social preview image.
4. Confirm GHCR image and chart package ownership, repository linkage, and
   anonymous visibility.
5. Publish KubeFacet v0.2.0 later through the protected, tag-gated release
   workflow after its required checks pass.
6. Register the project with Artifact Hub later.

These are post-merge maintainer actions. This migration performs no hosted
repository rename, remote update, public push, tag, GitHub Release, package
publication, or deletion of historical artifacts.
