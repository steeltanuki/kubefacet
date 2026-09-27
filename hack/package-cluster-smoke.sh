#!/usr/bin/env bash
# Copyright 2026 Alessandro Rontani
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

set -euo pipefail

readonly ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
readonly CHART_DIR="$ROOT_DIR/charts/kubefacet"
readonly TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/kubefacet-package-smoke.XXXXXXXX")"
version=""
kubeconfig=""
kube_context=""

while (($# > 0)); do
	case "$1" in
	--kubernetes-version)
		[[ $# -ge 2 ]] || { printf '%s\n' '--kubernetes-version requires a value' >&2; exit 64; }
		version="$2"
		shift 2
		;;
	--kubeconfig)
		[[ $# -ge 2 ]] || { printf '%s\n' '--kubeconfig requires a value' >&2; exit 64; }
		kubeconfig="$2"
		shift 2
		;;
	--context)
		[[ $# -ge 2 ]] || { printf '%s\n' '--context requires a value' >&2; exit 64; }
		kube_context="$2"
		shift 2
		;;
	*)
		printf 'unknown argument: %s\n' "$1" >&2
		exit 64
		;;
	esac
done

trap 'rm -rf -- "$TEMP_DIR"' EXIT

fail() {
	printf 'PACKAGE_COMPATIBILITY=complete STATUS=failed: %s\n' "$1" >&2
	exit 1
}

[[ "$version" == 1.35.6 || "$version" == 1.36.2 ]] || fail "unsupported Kubernetes version: $version"
[[ "$kubeconfig" == /* && -f "$kubeconfig" ]] || fail 'an existing absolute --kubeconfig is required'
[[ -n "$kube_context" ]] || fail 'an explicit --context is required'

for command_name in env go helm jq kubectl; do
	command -v "$command_name" >/dev/null 2>&1 || fail "required command is missing: $command_name"
done

readonly kubectl_args=(--kubeconfig "$kubeconfig" --context "$kube_context")
readonly helm_args=(--kubeconfig "$kubeconfig" --kube-context "$kube_context")
readonly namespace="$(printenv KUBEFACET_PACKAGE_NAMESPACE || printf '%s' kubefacet-system)"
readonly image_repository="$(printenv KUBEFACET_PACKAGE_IMAGE_REPOSITORY || true)"
readonly image_tag="$(printenv KUBEFACET_PACKAGE_IMAGE_TAG || true)"
readonly external_secret_name="$(printenv KUBEFACET_PACKAGE_EXTERNAL_SECRET_NAME || printf '%s' administrator-webhook-tls)"
readonly external_ca_bundle="$(printenv KUBEFACET_PACKAGE_EXTERNAL_CA_BUNDLE || true)"
readonly rotated_secret_manifest="$(printenv KUBEFACET_PACKAGE_EXTERNAL_ROTATED_SECRET || true)"
readonly rotated_ca_bundle="$(printenv KUBEFACET_PACKAGE_EXTERNAL_ROTATED_CA_BUNDLE || true)"
readonly author_namespace="$(printenv KUBEFACET_PACKAGE_AUTHOR_NAMESPACE || printf '%s' kubefacet-package-author)"
readonly author_name="$(printenv KUBEFACET_PACKAGE_AUTHOR_NAME || printf '%s' kubefacet-package-author)"
readonly canary_name="$(printenv KUBEFACET_PACKAGE_UNRELATED_CONFIGMAP || true)"
readonly canary_marker="$(printenv KUBEFACET_PACKAGE_UNRELATED_MARKER || true)"

[[ "$namespace" =~ ^[a-z0-9]([-a-z0-9]*[a-z0-9])?$ ]] || fail 'package namespace is not a DNS label'
[[ "$author_namespace" =~ ^[a-z0-9]([-a-z0-9]*[a-z0-9])?$ ]] || fail 'author namespace is not a DNS label'
[[ "$author_name" =~ ^[a-zA-Z0-9]([-a-zA-Z0-9_.]*[a-zA-Z0-9])?$ ]] || fail 'author identity is invalid'
[[ -n "$image_repository" && -n "$image_tag" && "$image_tag" != latest ]] || {
	printf '%s\n' 'live smoke requires an immutable KUBEFACET_PACKAGE_IMAGE_REPOSITORY and KUBEFACET_PACKAGE_IMAGE_TAG' >&2
	exit 64
}
[[ -n "$canary_name" && -n "$canary_marker" ]] || fail 'live smoke requires the run-owned unrelated ConfigMap canary'
[[ "$canary_name" =~ ^[a-z0-9]([-a-z0-9]*[a-z0-9])?$ ]] || fail 'unrelated ConfigMap name is not a DNS label'
[[ -f "$external_ca_bundle" && "$external_ca_bundle" == /* ]] || fail 'externalSecret smoke requires an existing absolute KUBEFACET_PACKAGE_EXTERNAL_CA_BUNDLE'
[[ -f "$rotated_ca_bundle" && "$rotated_ca_bundle" == /* ]] || fail 'externalSecret smoke requires an existing absolute KUBEFACET_PACKAGE_EXTERNAL_ROTATED_CA_BUNDLE'
[[ -f "$rotated_secret_manifest" && "$rotated_secret_manifest" == /* ]] || fail 'externalSecret smoke requires an existing absolute KUBEFACET_PACKAGE_EXTERNAL_ROTATED_SECRET'

kubectl_get() {
	env -u KUBECONFIG kubectl "${kubectl_args[@]}" "$@"
}

helm_release() {
	env -u KUBECONFIG helm "${helm_args[@]}" "$@"
}

apply_crds() {
	"$ROOT_DIR/hack/apply-compatible-crds.sh" "${kubectl_args[@]}"
}

assert_preservation_canary() {
	local actual
	actual="$(kubectl_get --namespace "$namespace" get configmap "$canary_name" \
		-o jsonpath='{.metadata.uid}|{.data.marker}')" || fail 'unrelated ConfigMap disappeared during package lifecycle'
	[[ "$actual" == "$canary_uid|$canary_marker" ]] || fail 'package lifecycle changed the unrelated ConfigMap UID or data'
}

uninstall_package() {
	local releases
	releases="$(helm_release list --namespace "$namespace" --filter '^kubefacet$' --output json)" ||
		fail 'could not inspect the Helm release before uninstall'
	case "$(jq 'length' <<<"$releases")" in
	0)
		return 0
		;;
	1)
		helm_release uninstall kubefacet --namespace "$namespace" --wait --timeout 10m >/dev/null ||
			fail 'normal package uninstall failed'
		;;
	*)
		fail 'unexpected duplicate Helm releases matched the package name'
		;;
	esac
}

assert_bootstrap_policy() {
	local policy
	policy="$(kubectl_get get facetaccesspolicy installation-access-ceiling -o json)" || fail 'managed access ceiling is missing'
	jq -e '
		.spec.namespaces.mode == "Explicit" and
		((.spec.namespaces.include // []) | length == 0) and
		((.spec.resources // []) | length == 0) and
		.spec.allowClusterScoped == false
	' <<<"$policy" >/dev/null || fail 'managed access ceiling is not the expected deny-all bootstrap'
}

assert_author_rbac() {
	local role
	role="$(kubectl_get --namespace "$author_namespace" get role kubefacet-author -o json)" || fail 'author Role was not installed'
	jq -e '
		([.rules[] | .resources[]] | sort) == ["facets", "facets/status"] and
		all(.rules[]; .apiGroups == ["kubefacet.steeltanuki.it"]) and
		all(.rules[]; all(.resources[]; . != "pods" and . != "secrets" and . != "deployments"))
	' <<<"$role" >/dev/null || fail 'author Role crosses the Facet API authorization boundary'
	[[ "$(kubectl_get auth can-i create facets.kubefacet.steeltanuki.it \
		--namespace "$author_namespace" --as "$author_name")" == yes ]] || fail 'configured author cannot create Facets'
	[[ "$(kubectl_get auth can-i get secrets \
		--namespace "$author_namespace" --as "$author_name")" == no ]] || fail 'configured author can read Secrets'
	[[ "$(kubectl_get auth can-i list pods \
		--namespace "$author_namespace" --as "$author_name")" == no ]] || fail 'configured author can list observed Pods'
}

wait_for_webhook_backends() {
	local attempt config endpoints
	for attempt in {1..90}; do
		if config="$(kubectl_get get validatingwebhookconfiguration kubefacet-validating-webhook -o json 2>/dev/null)" &&
			jq -e '(.webhooks | length == 2) and all(.webhooks[]; (.failurePolicy == "Fail") and ((.clientConfig.caBundle // "") | length > 0))' <<<"$config" >/dev/null &&
			endpoints="$(kubectl_get --namespace "$namespace" get endpointslices \
				--selector "kubernetes.io/service-name=kubefacet-webhook" -o json 2>/dev/null)" &&
			jq -e '[.items[].endpoints[]? | select(.conditions.ready == true or .conditions.ready == null)] | length > 0' <<<"$endpoints" >/dev/null; then
			return 0
		fi
		sleep 2
	done
	fail 'validating webhook CA or ready EndpointSlice backends did not become available'
}

assert_admission() {
	local phase="$1" safe_version valid_name invalid_name valid_manifest invalid_manifest rejection
	safe_version="$(tr '.' '-' <<<"$version" | tr -d '\n')"
	valid_name="package-smoke-$safe_version-$phase-valid"
	invalid_name="package-smoke-$safe_version-$phase-invalid"
	valid_manifest="$TEMP_DIR/$valid_name.yaml"
	invalid_manifest="$TEMP_DIR/$invalid_name.yaml"
	cat >"$valid_manifest" <<EOF
apiVersion: kubefacet.steeltanuki.it/v1alpha1
kind: Facet
metadata:
  name: $valid_name
  namespace: $namespace
spec:
  sources: []
EOF
	cat >"$invalid_manifest" <<EOF
apiVersion: kubefacet.steeltanuki.it/v1alpha1
kind: Facet
metadata:
  name: $invalid_name
  namespace: $namespace
spec:
  sources:
    - id: invalid
      resource:
        apiVersion: v1
        kind: "*"
EOF
	kubectl_get apply -f "$valid_manifest" >/dev/null || fail 'valid Facet was rejected by live admission'
	if rejection="$(kubectl_get apply -f "$invalid_manifest" 2>&1)"; then
		fail 'invalid Facet was accepted by live admission'
	fi
	[[ "$rejection" == *'spec.sources[0].resource.kind: Kind must be a valid CamelCase Kubernetes identifier'* ]] ||
		fail "invalid Facet failure did not report the semantic admission violation: $rejection"
	kubectl_get --namespace "$namespace" delete facet "$valid_name" --wait --ignore-not-found >/dev/null
}

assert_upgrade_rollback() {
	local initial_revision replicas history
	initial_revision="$(helm_release history kubefacet --namespace "$namespace" --output json \
		| jq -er 'map(.revision | tonumber) | min')" || fail 'initial Helm revision is missing'
	helm_release upgrade kubefacet "$CHART_DIR" --namespace "$namespace" --reuse-values \
		--set replicaCount=2 --wait --timeout 10m "$@" >/dev/null || fail 'live package upgrade failed'
	replicas="$(kubectl_get --namespace "$namespace" get deployment kubefacet -o jsonpath='{.spec.replicas}')"
	[[ "$replicas" == 2 ]] || fail 'live package upgrade did not apply the replica change'
	helm_release rollback kubefacet "$initial_revision" --namespace "$namespace" \
		--wait --timeout 10m >/dev/null || fail 'live package rollback failed'
	replicas="$(kubectl_get --namespace "$namespace" get deployment kubefacet -o jsonpath='{.spec.replicas}')"
	[[ "$replicas" == 1 ]] || fail 'live package rollback did not restore the original replica count'
	history="$(helm_release history kubefacet --namespace "$namespace" --output json \
		| jq 'length')"
	((history >= 3)) || fail 'live package upgrade and rollback did not create distinct release revisions'
	assert_bootstrap_policy
	assert_author_rbac
	assert_preservation_canary
}

run_profile() {
	local mode="$1"
	local canary_uid
	local values=(
		--set "image.repository=$image_repository"
		--set "image.tag=$image_tag"
		--set-json "rbac.authors.namespaces=[\"$author_namespace\"]"
		--set-json "rbac.authors.subjects=[{\"kind\":\"User\",\"name\":\"$author_name\"}]"
	)
	if [[ "$mode" == externalSecret ]]; then
		values+=(--set certificate.mode=externalSecret)
		values+=(--set "certificate.externalSecret.secretName=$external_secret_name")
		values+=(--set-file "certificate.externalSecret.caBundle=$external_ca_bundle")
		kubectl_get --namespace "$namespace" get secret "$external_secret_name" >/dev/null ||
			fail 'administrator-owned TLS Secret is missing before externalSecret installation'
	fi

	apply_crds
	kubectl_get get namespace "$author_namespace" >/dev/null 2>&1 ||
		kubectl_get create namespace "$author_namespace" >/dev/null
	canary_uid="$(kubectl_get --namespace "$namespace" get configmap "$canary_name" \
		-o jsonpath='{.metadata.uid}')"
	[[ -n "$canary_uid" ]] || fail 'unrelated ConfigMap canary is missing'

	helm_release upgrade --install kubefacet "$CHART_DIR" \
		--namespace "$namespace" --create-namespace \
		--wait --timeout 10m "${values[@]}" >/dev/null || fail "live install failed for $mode"
	kubectl_get wait --for=condition=Established --timeout=120s \
		crd/facets.kubefacet.steeltanuki.it crd/facetaccesspolicies.kubefacet.steeltanuki.it >/dev/null ||
		fail 'KubeFacet CRDs did not become Established'
	kubectl_get --namespace "$namespace" wait --for=condition=Available deployment/kubefacet --timeout=5m >/dev/null ||
		fail 'manager Deployment did not become Available'
	if [[ "$mode" == certManager ]]; then
		kubectl_get --namespace "$namespace" wait --for=condition=Ready certificate/kubefacet-webhook-serving --timeout=10m >/dev/null ||
			fail 'cert-manager did not issue the webhook serving certificate'
		kubectl_get --namespace "$namespace" get secret kubefacet-webhook-tls >/dev/null ||
			fail 'cert-manager serving Secret is missing'
	fi
	wait_for_webhook_backends
	assert_bootstrap_policy
	assert_author_rbac
	assert_admission initial
	assert_upgrade_rollback "${values[@]}"

	if [[ "$mode" == externalSecret ]]; then
		local before_generation after_generation
		before_generation="$(kubectl_get --namespace "$namespace" get deployment kubefacet -o jsonpath='{.metadata.generation}')"
		kubectl_get --namespace "$namespace" apply --server-side \
			--field-manager=kubefacet-external-secret-smoke -f "$rotated_secret_manifest" >/dev/null ||
			fail 'rotated administrator TLS Secret could not be applied'
		helm_release upgrade kubefacet "$CHART_DIR" --namespace "$namespace" --reuse-values \
			--set-file "certificate.externalSecret.caBundle=$rotated_ca_bundle" \
			--wait --timeout 10m >/dev/null || fail 'external CA bundle rotation upgrade failed'
		kubectl_get --namespace "$namespace" wait --for=condition=Available deployment/kubefacet --timeout=5m >/dev/null ||
			fail 'manager became unavailable during external TLS rotation'
		after_generation="$(kubectl_get --namespace "$namespace" get deployment kubefacet -o jsonpath='{.metadata.generation}')"
		[[ "$before_generation" == "$after_generation" ]] ||
			fail 'external certificate rotation unexpectedly changed the manager Deployment'
		assert_preservation_canary
		wait_for_webhook_backends
		assert_admission rotated
	fi

	assert_preservation_canary
	uninstall_package
	uninstall_package
	[[ "$(helm_release list --namespace "$namespace" --filter '^kubefacet$' --output json | jq 'length')" == 0 ]] ||
		fail 'repeated package uninstall did not converge'
	if kubectl_get get validatingwebhookconfiguration kubefacet-validating-webhook >/dev/null 2>&1; then
		fail 'normal uninstall retained the validating webhook configuration'
	fi
	if kubectl_get --namespace "$author_namespace" get role kubefacet-author >/dev/null 2>&1; then
		fail 'normal uninstall retained author RBAC'
	fi
	kubectl_get get crd facets.kubefacet.steeltanuki.it facetaccesspolicies.kubefacet.steeltanuki.it >/dev/null ||
		fail 'normal uninstall removed a retained CRD'
	assert_bootstrap_policy
	assert_preservation_canary
	if [[ "$mode" == externalSecret ]]; then
		kubectl_get --namespace "$namespace" get secret "$external_secret_name" >/dev/null ||
			fail 'normal uninstall removed the administrator-owned TLS Secret'
	fi

	local cluster_server purge_status purge_output invalid_token_output
	cluster_server="$(env -u KUBECONFIG kubectl config view --raw "${kubectl_args[@]}" -o json \
		| jq -er --arg context "$kube_context" '(.contexts[] | select(.name == $context) | .context.cluster) as $cluster | .clusters[] | select(.name == $cluster) | .cluster.server')"
	set +e
	invalid_token_output="$(GOCACHE="${GOCACHE:-/tmp/kubefacet-package-go-build}" \
		GOMODCACHE="${GOMODCACHE:-/tmp/kubefacet-package-go-mod}" \
		env -u KUBECONFIG go run ./cmd/kubefacet-purge \
		--kubeconfig "$kubeconfig" --context "$kube_context" \
		--confirm-context "$kube_context" --confirm-server "$cluster_server" \
		purge 2>&1)"
	purge_status=$?
	set -e
	((purge_status != 0)) || fail 'confirmed-purge executable accepted an invalid confirmation token'
	[[ "$invalid_token_output" == *'usage: kubefacet-purge'* ]] || fail 'invalid purge token did not reach the exact confirmation guard'
	purge_output="$(GOCACHE="${GOCACHE:-/tmp/kubefacet-package-go-build}" \
		GOMODCACHE="${GOMODCACHE:-/tmp/kubefacet-package-go-mod}" \
		env -u KUBECONFIG go run ./cmd/kubefacet-purge \
		--kubeconfig "$kubeconfig" --context "$kube_context" \
		--confirm-context "$kube_context" --confirm-server "$cluster_server" \
		purge-kubefacet-crds 2>&1)" || fail 'confirmed-purge command failed on the disposable package cluster'
	[[ "$purge_output" == *'PURGE_STATUS=passed'* ]] || fail 'confirmed-purge did not report success'
	if kubectl_get get crd facets.kubefacet.steeltanuki.it >/dev/null 2>&1; then
		fail 'confirmed-purge retained the Facet CRD'
	fi
	if kubectl_get get crd facetaccesspolicies.kubefacet.steeltanuki.it >/dev/null 2>&1; then
		fail 'confirmed-purge retained the FacetAccessPolicy CRD'
	fi
	if kubectl_get get facetaccesspolicy installation-access-ceiling >/dev/null 2>&1; then
		fail 'confirmed-purge retained the managed access ceiling'
	fi
	assert_preservation_canary
	if [[ "$mode" == externalSecret ]]; then
		kubectl_get --namespace "$namespace" get secret "$external_secret_name" >/dev/null ||
			fail 'confirmed-purge removed the administrator-owned TLS Secret'
	fi
	printf 'PACKAGE_CLUSTER_PROFILE version=%s mode=%s STATUS=passed\n' "$version" "$mode"
}

run_profile certManager
run_profile externalSecret
