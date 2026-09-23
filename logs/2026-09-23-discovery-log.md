# Read-only discovery log — 2026-09-23

## Purpose

Record what was inspected, why each tool was used, and the sanitized conclusion. Raw output is intentionally not stored because it contained environment-specific identifiers and potentially sensitive annotations.

## 1. Environment validation

Checked that `$AWS_REGION`, `$AWS_ACCOUNT_ID`, and `$CLUSTER_NAME` were populated before AWS operations. Values were not written to this repository.

## 2. Terraform inspection

Read:

- `terraform/variables.tf`
- `terraform/eks.tf`
- `terraform/vpc.tf`
- `terraform/alb.tf`
- `terraform/csi.tf`
- Terraform style guidance

Executed read-only state operations:

```bash
terraform state list
terraform state show '<selected-resource-address>'
```

Findings:

- EKS Auto Mode is enabled.
- Cluster, VPC, IAM, Pod Identity, AMP, ADOT, Grafana, DynamoDB, IngressClass, and StorageClass resources are managed by Terraform.
- Two private subnets exist across AZs.
- Only one public subnet is configured.
- Private subnets have internal-ELB discovery tags.
- The public subnet lacks the public-ELB discovery tag.

## 3. EKS control-plane inspection

Used EKS read APIs to inspect cluster, add-ons, node groups, and access entries.

Findings:

- Cluster is active on Kubernetes 1.34.
- Auto Mode compute, block storage, and load balancing are enabled.
- Zero traditional managed node groups and zero separately installed EKS add-ons were returned, which is expected for integrated Auto Mode capabilities.
- Public and private API endpoints are enabled.
- Public API CIDR currently allows all IPv4 sources.
- API/audit/authenticator logging and KMS Secret encryption are enabled.

## 4. Kubernetes API discovery

Listed API versions before reading resources. Relevant APIs included:

- `v1`
- `apps/v1`
- `networking.k8s.io/v1`
- `storage.k8s.io/v1`
- `karpenter.sh/v1`
- `eks.amazonaws.com/v1`

Several MCP list requests were rate-limited. A consolidated read-only `kubectl get` fallback was used and explicitly identified as a fallback.

## 5. Data-plane inspection

Findings:

- One ready Auto Mode Bottlerocket node.
- One active general-purpose NodePool and zero nodes in the system NodePool.
- Ten ready application/observability Pods with no observed restarts.
- Node and Pod addresses are VPC-native.
- All workloads were concentrated on one node/AZ.

## 6. Service and Ingress inspection

Findings:

- Application Services are internal ClusterIP Services.
- The UI Service selects the UI Pod and maps port 80 to its named application port.
- The UI Ingress requests an internet-facing ALB with IP targets.
- Ingress status contains no load-balancer address.

Ingress events reported 157 failures because subnet auto-discovery found one subnet while two are required.

## 7. Pod Identity inspection

Read the carts ServiceAccount, Terraform association, IAM trust policy, and permission policy.

Findings:

- Namespace and ServiceAccount are associated with a workload IAM role.
- Trust is delegated to `pods.eks.amazonaws.com`.
- DynamoDB permissions are resource-scoped rather than wildcarded.

No tokens or temporary credentials were read.

## 8. Storage inspection

Findings:

- Default Auto Mode EBS StorageClass uses encrypted GP3, expansion, and `WaitForFirstConsumer`.
- No PVC or PV exists.
- Sample database data uses Pod-lifetime `emptyDir` storage.
- A plaintext sensitive value was visible in a workload specification; it is not reproduced here.

## 9. Documentation verification

Checked current AWS EKS documentation for:

- control-plane architecture
- Auto Mode networking and integrated components
- Pod-native VPC networking
- Auto Mode ALB/NLB classes
- public/private subnet discovery tags
- minimum two-AZ ALB subnet placement

## 10. Mutation decision

No remediation was executed. VPC changes, Ingress recreation, public load-balancer creation, and storage changes require explicit approval because they can affect connectivity, availability, security, data, and cost.