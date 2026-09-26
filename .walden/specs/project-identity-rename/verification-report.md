# KubeFacet Identity Migration Verification Report

## Scope and evidence boundary

Record the selected-feature scope, approved specification fingerprints, final
commit, and the distinction between migration evidence and historical feature
evidence. Do not claim portfolio-wide certification.

## Declared checkpoints and actual outcomes

For every required checkpoint, record the exact command, whether it ran, its
pass/fail result, and any named output marker. Identify checks not yet run.

## Regenerated artifacts

List generated API code, CRDs, chart copies, checksum metadata, container and
release metadata, and the command that reproduced each artifact.

## Repository identity residue

Record the final audit file/occurrence counts, historical hashes, every
classified migration explanation and path with its reason, and the result of
the isolated negative-injection cases. No operational residue may be reported
as acceptable.

## Commit boundaries

List the specification, API/runtime, packaging/distribution/local/examples,
current-documentation, and final-evidence commits with their scope and order.

## Manual actions after merge

Record the repository rename, local remote update, GitHub profile review, GHCR
visibility review, later v0.2.0 publication, and later Artifact Hub
registration as maintainer work outside this migration.

## Walden delivery checkpoint

Record `walden verify project-identity-rename --json` and the strict selected-
feature `walden release check project-identity-rename --strict --json` result.
