# 8. Hands-on labs

Labs 1–6 are read-only. Labs marked **approval required** can change resources, availability, public exposure, or cost and must first be reviewed through Terraform or manifest review.

## Lab 1: Map AWS and Kubernetes layers

```bash
aws eks describe-cluster \
  --region "$AWS_REGION" \
  --name "$CLUSTER_NAME" \
  --query 'cluster.{Version:version,Status:status,Access:accessConfig,Compute:computeConfig,Storage:storageConfig,Networking:kubernetesNetworkConfig}'

kubectl get nodes -L eks.amazonaws.com/compute-type,karpenter.sh/nodepool
kubectl get nodepool
kubectl get nodeclass
```

Confirm Auto Mode, NodePool-to-NodeClass references, ready nodes, and capacity type.

## Lab 2: Trace Deployment to container

```bash
kubectl get deployment,replicaset,pod -n retail-store \
  -l app.kubernetes.io/name=ui
kubectl describe deployment ui -n retail-store
kubectl get pod -n retail-store \
  -l app.kubernetes.io/name=ui \
  -o custom-columns='POD:.metadata.name,NODE:.spec.nodeName,IP:.status.podIP,READY:.status.containerStatuses[*].ready'
```

Trace owner references:

```text
Deployment → ReplicaSet → Pod → container
```

## Lab 3: Trace Service discovery

```bash
kubectl get service ui -n retail-store -o wide
kubectl get endpointslice -n retail-store \
  -l kubernetes.io/service-name=ui -o wide
kubectl get pod -n retail-store \
  -l app.kubernetes.io/name=ui --show-labels
```

Verify that the Service selector matches the Pod labels and that only ready endpoints receive traffic.

## Lab 4: Inspect Pod Identity without exposing credentials

```bash
aws eks list-pod-identity-associations \
  --region "$AWS_REGION" \
  --cluster-name "$CLUSTER_NAME"

kubectl get serviceaccount carts -n retail-store -o yaml
kubectl get deployment carts -n retail-store \
  -o jsonpath='{.spec.template.spec.serviceAccountName}{"\n"}'
```

Inspect the associated IAM role policy separately, but do not copy ARNs or credential output into this repository.

Expected relationship:

```text
Deployment uses ServiceAccount
  → EKS association matches namespace/ServiceAccount
  → IAM role trust allows pods.eks.amazonaws.com
  → policy grants only application-required resources/actions
```

## Lab 5: Inspect storage durability

```bash
kubectl get storageclass
kubectl get pvc -A
kubectl get pv
kubectl get statefulset catalog-mysql -n retail-store \
  -o jsonpath='{.spec.template.spec.volumes}{"\n"}'
```

Decide whether each workload uses ephemeral storage, EBS, EFS, or a managed data service. Never assume a StatefulSet is persistent merely because it has a stable Pod name.

## Lab 6: Diagnose the existing Ingress

```bash
kubectl get ingress ui -n retail-store -o wide
kubectl describe ingress ui -n retail-store
kubectl get events -n retail-store \
  --field-selector involvedObject.kind=Ingress,involvedObject.name=ui \
  --sort-by='.lastTimestamp'
```

Trace:

```text
Ingress → IngressClass → IngressClassParams
        → subnet discovery → ALB → target group
        → Service → EndpointSlice → ready Pod
```

## Lab 7: Correct ALB subnet discovery — approval required

Before changing anything:

1. Decide whether the application should be internet-facing or internal.
2. Review `terraform/vpc.tf` and `terraform/alb.tf`.
3. Review `terraform/variables.tf`.
4. Ensure an internet-facing ALB has tagged public subnets in two AZs.
5. Run a Terraform plan with the environment cluster name.
6. Stop if any resource will be destroyed.
7. Explain every update-in-place and replacement.
8. Apply only after explicit approval.
9. Recreate the Ingress after subnet changes so discovery runs again.
10. Wait at least 150 seconds after the ALB reports active before testing.

Plan command:

```bash
terraform plan -var="cluster_name=$CLUSTER_NAME"
```

Do not copy account-specific plan output into this repository without sanitizing it.

## Lab 8: Persistent EBS claim — approval required

Review the example in `05-storage.md`. Before applying, decide:

- required capacity
- access mode
- backup/snapshot strategy
- encryption key policy
- reclaim/retention behavior
- failure and restore test

After approval, validate the lifecycle:

```bash
kubectl get pvc,pv -n retail-store
kubectl describe pvc application-data -n retail-store
kubectl get events -n retail-store --sort-by='.lastTimestamp'
```

Deleting a PVC may delete the EBS volume when the StorageClass reclaim policy is `Delete`.

## Lab 9: Availability design — approval required

For production-like availability, review:

- at least two application replicas
- PodDisruptionBudget
- topology spread across zones/hosts
- readiness and startup probes
- realistic CPU/memory requests
- Auto Mode NodePool disruption settings

Validate scheduling with:

```bash
kubectl get pods -n retail-store \
  -o custom-columns='POD:.metadata.name,NODE:.spec.nodeName,ZONE:.metadata.labels.topology\.kubernetes\.io/zone'
```

## Lab completion checklist

- Explain control plane versus data plane without referring to a diagram.
- Trace a `kubectl` request through IAM and RBAC.
- Trace a packet through DNS, Service, EndpointSlice, and Pod.
- Explain why Pod Identity is safer than node-role permissions.
- Predict whether data survives Pod, node, and AZ failure.
- Select ALB or NLB based on protocol and routing requirements.
- Diagnose an empty Ingress address using events and subnet discovery prerequisites.