#!/usr/bin/env bash
# Copyright 2026 Alessandro Rontani
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

set -euo pipefail

readonly ROOT_DIR="$(cd -- "$(dirname -- "$0")/.." && pwd)"
TEMP_PARENT="$(printenv TMPDIR || printf '%s' /tmp)"
[[ "$TEMP_PARENT" == /* && -d "$TEMP_PARENT" && -w "$TEMP_PARENT" ]] || {
	printf 'package proof TMPDIR must be an existing writable absolute path: %s\n' "$TEMP_PARENT" >&2
	exit 64
}
readonly RUN_DIR="$(mktemp -d "$TEMP_PARENT/kubefacet-package-cluster.XXXXXXXX")"
readonly RUN_ID="$(date -u +%Y%m%d%H%M%S)-$$"
readonly SOURCE_REVISION="$(git -C "$ROOT_DIR" rev-parse --verify HEAD)"
readonly IMAGE_REPOSITORY="localhost/kubefacet-package-proof"
readonly IMAGE_TAG="package-proof-$RUN_ID"
readonly IMAGE_REF="$IMAGE_REPOSITORY:$IMAGE_TAG"
readonly PACKAGE_NAMESPACE="kubefacet-system"
readonly AUTHOR_NAMESPACE="kubefacet-author-$RUN_ID"
readonly AUTHOR_NAME="kubefacet-package-author-$RUN_ID"
readonly CANARY_NAME="kubefacet-package-preserve-$RUN_ID"
readonly CANARY_MARKER="package-preservation-$RUN_ID"
readonly SECRET_NAME="administrator-webhook-tls"
readonly EXTERNAL_CA_BUNDLE="$RUN_DIR/ca-initial.pem"
readonly ROTATED_CA_BUNDLE="$RUN_DIR/ca-rotated.pem"
readonly ROTATED_SECRET="$RUN_DIR/secret-rotated.yaml"
readonly MODULE_CACHE="$(go env GOMODCACHE)"
readonly GO_BUILD_CACHE="$(printenv GOCACHE || printf '%s/go-build' "$RUN_DIR")"
readonly PROFILE_LOG="$RUN_DIR/package-profiles.log"

source "$ROOT_DIR/hack/kind-podman-common.sh"

active_cluster_name=""
active_kubeconfig=""
active_context=""
active_nodes=""
active_version=""
cluster_owned=0
image_built=0
image_id=""
proof_succeeded=0
preserve_run_dir=0
cleanup_status=0

run_kind() {
	kp_run_kind podman "$@"
}

run_podman() {
	kp_run_podman "$@"
}

run_kubectl() {
	local kubeconfig="$1" context="$2"
	shift 2
	kp_run_kubectl "$kubeconfig" "$context" "$@"
}

fail() {
	printf 'PROJECT_IDENTITY=package-cluster STATUS=failed: %s\n' "$1" >&2
	exit 1
}

toolchain_value() {
	local key="$1" fallback="$2" value
	value="$(awk -v key="$key" '$1 == key { print $3; exit }' "$ROOT_DIR/hack/toolchain.mk")"
	if [[ -n "$value" ]]; then
		printf '%s\n' "$value"
	else
		printf '%s\n' "$fallback"
	fi
}

capture_worktree_snapshot() {
	local destination="$1"
	mkdir -p -- "$destination"
	git -C "$ROOT_DIR" status --porcelain=v1 --untracked-files=all >"$destination/status"
	git -C "$ROOT_DIR" diff --no-ext-diff --binary HEAD >"$destination/diff"
	git -C "$ROOT_DIR" diff --cached --no-ext-diff --binary >"$destination/cached-diff"
	git -C "$ROOT_DIR" rev-parse --verify HEAD >"$destination/revision"
}

assert_worktree_unchanged() {
	local before="$RUN_DIR/worktree.before" after="$RUN_DIR/worktree.after"
	capture_worktree_snapshot "$after"
	cmp -s "$before/status" "$after/status" &&
		cmp -s "$before/diff" "$after/diff" &&
		cmp -s "$before/cached-diff" "$after/cached-diff" &&
		cmp -s "$before/revision" "$after/revision"
}

cluster_exists() {
	local cluster_name="$1" current_clusters
	current_clusters="$(run_kind get clusters)"
	printf '%s\n' "$current_clusters" | rg -F -x -q -- "$cluster_name"
}

remove_active_cluster() {
	local node current_nodes
	((cluster_owned)) || return 0
	if cluster_exists "$active_cluster_name"; then
		if ! run_kind delete cluster --name "$active_cluster_name" --kubeconfig "$active_kubeconfig" \
			>"$RUN_DIR/cluster-delete.log" 2>&1; then
			tail -n 60 "$RUN_DIR/cluster-delete.log" >&2 || true
			cleanup_status=1
			preserve_run_dir=1
			return 1
		fi
	fi
	if cluster_exists "$active_cluster_name"; then
		printf 'owned kind cluster survived deletion: %s\n' "$active_cluster_name" >&2
		cleanup_status=1
		preserve_run_dir=1
		return 1
	fi
	current_nodes="$(run_podman ps --all --format '{{.Names}}')"
	while IFS= read -r node; do
		[[ -n "$node" ]] || continue
		if printf '%s\n' "$current_nodes" | rg -F -x -q -- "$node"; then
			printf 'owned kind node survived cluster cleanup: %s\n' "$node" >&2
			cleanup_status=1
			preserve_run_dir=1
			return 1
		fi
	done <<<"$active_nodes"
	cluster_owned=0
	active_cluster_name=""
	active_kubeconfig=""
	active_context=""
	active_nodes=""
	active_version=""
}

cleanup() {
	local status="$?" existing_image_id
	trap - EXIT
	if ((cluster_owned)); then
		remove_active_cluster || true
	fi
	if ((image_built)); then
		existing_image_id="$(run_podman image inspect --format '{{.Id}}' "$IMAGE_REF" 2>/dev/null || true)"
		if [[ "$existing_image_id" == "$image_id" ]]; then
			if ! run_podman image rm "$IMAGE_REF" >/dev/null 2>&1; then
				printf 'could not remove run-owned Podman image %s\n' "$IMAGE_REF" >&2
				cleanup_status=1
				preserve_run_dir=1
			fi
		elif [[ -n "$existing_image_id" ]]; then
			printf 'run-owned image tag changed unexpectedly: %s\n' "$IMAGE_REF" >&2
			cleanup_status=1
			preserve_run_dir=1
		fi
	fi
	if ! assert_worktree_unchanged; then
		printf '%s\n' 'package proof changed the source worktree' >&2
		cleanup_status=1
	fi
	if ((cleanup_status != 0)); then
		status=1
	fi
	if ((proof_succeeded && status == 0)); then
		printf 'PROJECT_IDENTITY=package-cluster STATUS=passed PROFILES=4\n'
	fi
	if ((preserve_run_dir)); then
		printf 'PACKAGE_CLUSTER_CLEANUP=retained path=%s cluster=%s context=%s\n' \
			"$RUN_DIR" "$active_cluster_name" "$active_context" >&2
	else
		chmod -R u+w -- "$RUN_DIR" 2>/dev/null || true
		rm -rf -- "$RUN_DIR"
	fi
	exit "$status"
}
trap cleanup EXIT

preflight() {
	local command_name rootless
	case "$(uname -s):$(uname -m)" in
	Linux:x86_64|Linux:amd64) ;;
	*) fail 'genuine package proof requires Linux/amd64' ;;
	esac
	for command_name in go git kind podman kubectl helm curl openssl jq base64; do
		command -v "$command_name" >/dev/null 2>&1 || fail "required command is missing: $command_name"
	done
	rootless="$(run_podman info --format '{{.Host.Security.Rootless}}')" || fail 'Podman info failed'
	[[ "$rootless" == true ]] || fail 'genuine package proof requires rootless Podman'
	[[ "$MODULE_CACHE" == /* && -d "$MODULE_CACHE" ]] || fail 'Go module cache is unavailable'
}

node_image_for_version() {
	case "$1" in
	1.35.6) printf '%s\n' "$(printenv KIND_NODE_IMAGE_1_35_6 || toolchain_value KIND_NODE_IMAGE_1_35_6 kindest/node:v1.35.5)" ;;
	1.36.2) printf '%s\n' "$(printenv KIND_NODE_IMAGE_1_36_2 || toolchain_value KIND_NODE_IMAGE_1_36_2 kindest/node:v1.36.1)" ;;
	*) fail "unsupported Kubernetes version: $1" ;;
	esac
}

generate_external_secret_fixtures() {
	local certificates="$RUN_DIR/certificates" serial ca key csr certificate extensions certificate_data key_data
	mkdir -p -- "$certificates"
	for serial in initial rotated; do
		ca="$certificates/$serial-ca.crt"
		key="$certificates/$serial-tls.key"
		csr="$certificates/$serial-tls.csr"
		certificate="$certificates/$serial-tls.crt"
		extensions="$certificates/$serial-ext.cnf"
		openssl req -x509 -newkey rsa:2048 -nodes -keyout "$certificates/$serial-ca.key" \
			-out "$ca" -days 7 -subj "/CN=KubeFacet Package Proof $serial CA" \
			-addext 'basicConstraints=critical,CA:TRUE' \
			-addext 'keyUsage=critical,keyCertSign,cRLSign' >/dev/null 2>&1
		openssl req -newkey rsa:2048 -nodes -keyout "$key" -out "$csr" \
			-subj '/CN=kubefacet-webhook.kubefacet-system.svc' >/dev/null 2>&1
		cat >"$extensions" <<'EOF'
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:kubefacet-webhook,DNS:kubefacet-webhook.kubefacet-system,DNS:kubefacet-webhook.kubefacet-system.svc,DNS:kubefacet-webhook.kubefacet-system.svc.cluster.local
EOF
		openssl x509 -req -in "$csr" -CA "$ca" -CAkey "$certificates/$serial-ca.key" \
			-CAcreateserial -days 7 -sha256 -extfile "$extensions" -out "$certificate" >/dev/null 2>&1
	done
	cat "$certificates/initial-ca.crt" >"$EXTERNAL_CA_BUNDLE"
	cat "$certificates/initial-ca.crt" "$certificates/rotated-ca.crt" >"$ROTATED_CA_BUNDLE"
	certificate_data="$(base64 -w0 "$certificates/rotated-tls.crt")"
	key_data="$(base64 -w0 "$certificates/rotated-tls.key")"
	cat >"$ROTATED_SECRET" <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: $SECRET_NAME
  namespace: $PACKAGE_NAMESPACE
type: kubernetes.io/tls
data:
  tls.crt: $certificate_data
  tls.key: $key_data
EOF
	certificate_data="$(base64 -w0 "$certificates/initial-tls.crt")"
	key_data="$(base64 -w0 "$certificates/initial-tls.key")"
	cat >"$RUN_DIR/secret-initial.yaml" <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: $SECRET_NAME
  namespace: $PACKAGE_NAMESPACE
type: kubernetes.io/tls
data:
  tls.crt: $certificate_data
  tls.key: $key_data
EOF
}

build_manager_once() {
	local chart_version
	chart_version="$(awk '$1 == "appVersion:" { gsub(/"/, "", $2); print $2; exit }' \
		"$ROOT_DIR/charts/kubefacet/Chart.yaml")"
	[[ -n "$chart_version" ]] || fail 'chart appVersion is missing'
	if ! run_podman build --file "$ROOT_DIR/Dockerfile" --tag "$IMAGE_REF" \
		--build-arg "VERSION=$chart_version" \
		--build-arg "COMMIT=$SOURCE_REVISION" \
		--build-arg "BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
		"$ROOT_DIR" >"$RUN_DIR/image-build.log" 2>&1; then
		tail -n 80 "$RUN_DIR/image-build.log" >&2 || true
		fail 'current manager image build failed'
	fi
	image_id="$(run_podman image inspect --format '{{.Id}}' "$IMAGE_REF")" || fail 'Podman could not inspect the built manager image'
	[[ -n "$image_id" ]] || fail 'Podman returned an empty manager image identity'
	image_built=1
	run_podman save --format oci-archive --output "$RUN_DIR/kubefacet-manager.oci.tar" "$IMAGE_REF" \
		>"$RUN_DIR/image-save.log" 2>&1 || fail 'Podman could not save the manager image archive'
	[[ -s "$RUN_DIR/kubefacet-manager.oci.tar" ]] || fail 'manager image archive is empty'
}

load_manager_into_active_cluster() {
	local node node_archive
	active_nodes="$(run_kind get nodes --name "$active_cluster_name")" || fail 'kind could not list the owned nodes'
	[[ -n "$active_nodes" ]] || fail 'kind returned no nodes for the owned package cluster'
	while IFS= read -r node; do
		[[ -n "$node" ]] || continue
		node_archive="/tmp/kubefacet-package-$RUN_ID.oci.tar"
		run_podman cp "$RUN_DIR/kubefacet-manager.oci.tar" "$node:$node_archive" \
			>"$RUN_DIR/image-copy.log" 2>&1 || fail "could not copy manager image into $node"
		run_podman exec "$node" ctr --namespace k8s.io images import "$node_archive" \
			>"$RUN_DIR/image-import.log" 2>&1 || fail "could not import manager image into $node"
		run_podman exec "$node" rm -f "$node_archive" >/dev/null 2>&1 || fail "could not remove image archive from $node"
	done <<<"$active_nodes"
}

install_cert_manager() {
	run_kubectl "$active_kubeconfig" "$active_context" apply --server-side \
		--field-manager=kubefacet-package-cert-manager -f "$RUN_DIR/cert-manager.yaml" \
		>"$RUN_DIR/cert-manager-apply.log" 2>&1 || {
			tail -n 60 "$RUN_DIR/cert-manager-apply.log" >&2 || true
			fail "cert-manager installation failed on Kubernetes $active_version"
		}
	run_kubectl "$active_kubeconfig" "$active_context" wait --for=condition=Established --timeout=5m \
		crd/certificates.cert-manager.io crd/issuers.cert-manager.io crd/clusterissuers.cert-manager.io \
		>"$RUN_DIR/cert-manager-crds.log" 2>&1 || {
			tail -n 60 "$RUN_DIR/cert-manager-crds.log" >&2 || true
			fail "cert-manager CRDs did not become Established on Kubernetes $active_version"
		}
	run_kubectl "$active_kubeconfig" "$active_context" --namespace cert-manager wait \
		--for=condition=Available deployment --all --timeout=10m \
		>"$RUN_DIR/cert-manager-ready.log" 2>&1 || {
			tail -n 60 "$RUN_DIR/cert-manager-ready.log" >&2 || true
			fail "cert-manager did not become Available on Kubernetes $active_version"
		}
}

prepare_active_cluster() {
	local version="$1" safe_version cluster_image cluster_list
	safe_version="$(tr '.' '-' <<<"$version" | tr -d '\n')"
	cluster_image="$(node_image_for_version "$version")"
	active_cluster_name="kubefacet-package-$RUN_ID-$safe_version"
	active_context="kind-$active_cluster_name"
	active_kubeconfig="$RUN_DIR/$safe_version.kubeconfig"
	active_version="$version"
	cluster_list="$(run_kind get clusters)"
	if printf '%s\n' "$cluster_list" | rg -F -x -q -- "$active_cluster_name"; then
		fail "run-unique package cluster already exists: $active_cluster_name"
	fi
	cluster_owned=1
	if ! run_kind create cluster --name "$active_cluster_name" --image "$cluster_image" \
		--wait 5m --kubeconfig "$active_kubeconfig" >"$RUN_DIR/cluster-create.log" 2>&1; then
		tail -n 80 "$RUN_DIR/cluster-create.log" >&2 || true
		fail "kind cluster creation failed for Kubernetes $version"
	fi
	[[ -s "$active_kubeconfig" ]] || fail "kind did not write the owned kubeconfig for Kubernetes $version"
	load_manager_into_active_cluster
	install_cert_manager
	run_kubectl "$active_kubeconfig" "$active_context" create namespace "$PACKAGE_NAMESPACE" >/dev/null
	run_kubectl "$active_kubeconfig" "$active_context" create namespace "$AUTHOR_NAMESPACE" >/dev/null
	run_kubectl "$active_kubeconfig" "$active_context" --namespace "$PACKAGE_NAMESPACE" \
		create configmap "$CANARY_NAME" --from-literal="marker=$CANARY_MARKER" >/dev/null
	run_kubectl "$active_kubeconfig" "$active_context" --namespace "$PACKAGE_NAMESPACE" \
		apply --server-side --field-manager=kubefacet-external-secret-smoke \
		-f "$RUN_DIR/secret-initial.yaml" >/dev/null
}

run_package_matrix_for_active_cluster() {
	local safe_version kubeconfig_1_35_6 context_1_35_6 kubeconfig_1_36_2 context_1_36_2 log
	safe_version="$(tr '.' '-' <<<"$active_version" | tr -d '\n')"
	kubeconfig_1_35_6=""
	context_1_35_6=""
	kubeconfig_1_36_2=""
	context_1_36_2=""
	if [[ "$active_version" == 1.35.6 ]]; then
		kubeconfig_1_35_6="$active_kubeconfig"
		context_1_35_6="$active_context"
	else
		kubeconfig_1_36_2="$active_kubeconfig"
		context_1_36_2="$active_context"
	fi
	log="$RUN_DIR/package-$safe_version.log"
	if ! (
		cd "$ROOT_DIR"
		env -u KUBECONFIG \
			GOCACHE="$GO_BUILD_CACHE" GOMODCACHE="$MODULE_CACHE" \
			KUBEFACET_PACKAGE_RUN_CLUSTER=1 \
			KUBEFACET_PACKAGE_CONFIRM_DISPOSABLE=purge-kubefacet-crds \
			KUBEFACET_PACKAGE_CLUSTER_VERSION="$active_version" \
			KUBEFACET_PACKAGE_KUBECONFIG_1_35_6="$kubeconfig_1_35_6" \
			KUBEFACET_PACKAGE_CONTEXT_1_35_6="$context_1_35_6" \
			KUBEFACET_PACKAGE_KUBECONFIG_1_36_2="$kubeconfig_1_36_2" \
			KUBEFACET_PACKAGE_CONTEXT_1_36_2="$context_1_36_2" \
			KUBEFACET_PACKAGE_NAMESPACE="$PACKAGE_NAMESPACE" \
			KUBEFACET_PACKAGE_IMAGE_REPOSITORY="$IMAGE_REPOSITORY" \
			KUBEFACET_PACKAGE_IMAGE_TAG="$IMAGE_TAG" \
			KUBEFACET_PACKAGE_EXTERNAL_SECRET_NAME="$SECRET_NAME" \
			KUBEFACET_PACKAGE_EXTERNAL_CA_BUNDLE="$EXTERNAL_CA_BUNDLE" \
			KUBEFACET_PACKAGE_EXTERNAL_ROTATED_SECRET="$ROTATED_SECRET" \
			KUBEFACET_PACKAGE_EXTERNAL_ROTATED_CA_BUNDLE="$ROTATED_CA_BUNDLE" \
			KUBEFACET_PACKAGE_AUTHOR_NAMESPACE="$AUTHOR_NAMESPACE" \
			KUBEFACET_PACKAGE_AUTHOR_NAME="$AUTHOR_NAME" \
			KUBEFACET_PACKAGE_UNRELATED_CONFIGMAP="$CANARY_NAME" \
			KUBEFACET_PACKAGE_UNRELATED_MARKER="$CANARY_MARKER" \
			make --no-print-directory test-package-compatibility
	) >"$log" 2>&1; then
		tail -n 100 "$log" >&2 || true
		fail "package compatibility smoke failed on Kubernetes $active_version"
	fi
	grep -F -x 'PACKAGE_COMPATIBILITY=complete STATUS=passed' "$log" >/dev/null ||
		fail "render matrix did not report completion on Kubernetes $active_version"
	for mode in certManager externalSecret; do
		grep -F -x "PACKAGE_CLUSTER_PROFILE version=$active_version mode=$mode STATUS=passed" "$log" >/dev/null ||
			fail "missing $mode live profile on Kubernetes $active_version"
	done
	[[ "$(grep -c '^PACKAGE_CLUSTER_PROFILE ' "$log")" == 2 ]] ||
		fail "unexpected live profile count on Kubernetes $active_version"
	grep -E '^PACKAGE_CLUSTER_PROFILE |^PACKAGE_COMPATIBILITY=' "$log" | tee -a "$PROFILE_LOG"
}

mkdir -p -- "$RUN_DIR"
capture_worktree_snapshot "$RUN_DIR/worktree.before"
: >"$PROFILE_LOG"
preflight
CERT_MANAGER_VERSION="$(printenv CERT_MANAGER_VERSION || toolchain_value CERT_MANAGER_VERSION v1.18.2)"
readonly CERT_MANAGER_VERSION
CERT_MANAGER_URL="https://github.com/cert-manager/cert-manager/releases/download/$CERT_MANAGER_VERSION/cert-manager.yaml"
if ! curl --fail --silent --show-error --location --retry 3 \
	--output "$RUN_DIR/cert-manager.yaml" "$CERT_MANAGER_URL"; then
	fail "could not download pinned cert-manager manifest $CERT_MANAGER_VERSION"
fi
[[ -s "$RUN_DIR/cert-manager.yaml" ]] || fail 'downloaded cert-manager manifest is empty'
generate_external_secret_fixtures
build_manager_once
prepare_active_cluster 1.35.6
run_package_matrix_for_active_cluster
remove_active_cluster
prepare_active_cluster 1.36.2
run_package_matrix_for_active_cluster
remove_active_cluster
[[ "$(grep -c '^PACKAGE_CLUSTER_PROFILE ' "$PROFILE_LOG")" == 4 ]] ||
	fail 'supported package matrix did not pass all four certificate/version profiles'
[[ "$(grep -c '^PACKAGE_COMPATIBILITY=complete STATUS=passed$' "$PROFILE_LOG")" == 2 ]] ||
	fail 'render compatibility did not complete for both version-specific live invocations'
proof_succeeded=1
