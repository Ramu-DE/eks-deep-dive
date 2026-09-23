#!/usr/bin/env bash
set -euo pipefail

: "${AWS_REGION:?AWS_REGION must be set}"
: "${AWS_ACCOUNT_ID:?AWS_ACCOUNT_ID must be set}"
: "${CLUSTER_NAME:?CLUSTER_NAME must be set}"

TERRAFORM_DIR="${TERRAFORM_DIR:-../terraform}"

heading() {
  printf '\n=== %s ===\n' "$1"
}

heading "EKS summary"
aws eks describe-cluster \
  --region "$AWS_REGION" \
  --name "$CLUSTER_NAME" \
  --query 'cluster.{Version:version,Status:status,Access:accessConfig,Compute:{Enabled:computeConfig.enabled,NodePools:computeConfig.nodePools},Storage:storageConfig,Network:kubernetesNetworkConfig,EndpointAccess:{Public:resourcesVpcConfig.endpointPublicAccess,Private:resourcesVpcConfig.endpointPrivateAccess,PublicCidrs:resourcesVpcConfig.publicAccessCidrs}}'

heading "kubectl compatibility"
kubectl version

heading "Authorization probes"
kubectl auth can-i get pods -A
kubectl auth can-i list nodes

heading "Namespaces and workload controllers"
kubectl get namespaces
kubectl get deployments,statefulsets -A

heading "Node count and scheduling classes"
printf 'Ready/total nodes: '
kubectl get nodes --no-headers | awk '{total++; if ($2 == "Ready") ready++} END {printf "%d/%d\n", ready+0, total+0}'
kubectl get nodepool
kubectl get nodeclass

heading "Services and exposure"
kubectl get services -A
kubectl get ingress -A

heading "Storage"
kubectl get storageclass
kubectl get pvc -A
kubectl get pv

heading "Recent warnings"
kubectl get events -A --field-selector type=Warning --sort-by='.lastTimestamp'

if [[ -d "$TERRAFORM_DIR" ]]; then
  heading "Terraform resource addresses"
  terraform -chdir="$TERRAFORM_DIR" state list
else
  printf '\nTerraform directory not found: %s\n' "$TERRAFORM_DIR" >&2
fi

cat <<'NOTICE'

Discovery complete. Output can contain environment-specific names.
Review and sanitize it before saving or sharing. Never commit raw Terraform
state, kubeconfig content, tokens, credentials, Secret data, or ARNs.
NOTICE
