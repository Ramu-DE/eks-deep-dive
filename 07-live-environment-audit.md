# 7. Sanitized live-environment audit

**Discovery date:** 2026-09-23 UTC  
**Mode:** Read-only  
**Scope:** Terraform state, EKS configuration, Kubernetes objects, IAM role policy, events, and current AWS documentation.

## Sanitization

This report excludes account IDs, ARNs, access-key identifiers, endpoint URLs, certificate data, role session names, resource IDs, Pod/node names, and Secret values. It is safe to use as documentation, but should still receive human review before publication.

## Cluster

- Kubernetes server version: `1.34`.
- EKS Auto Mode enabled.
- Status: active.
- Public and private Kubernetes API endpoints enabled.
- Public API endpoint network allow-list currently includes all IPv4 addresses.
- API, audit, and authenticator control-plane logs enabled.
- Scheduler and controller-manager logs not enabled.
- Kubernetes Secrets encrypted with a customer-managed KMS key.
- Authentication mode supports EKS API access entries and legacy ConfigMap mappings.

## Compute

- One ready Auto Mode Bottlerocket node was observed.
- Instance class observed: compute-optimized, two vCPU, approximately four GiB memory.
- One `general-purpose` NodePool has a node; the `system` NodePool has zero.
- Capacity is on-demand and Linux/amd64.
- NodePool consolidation is enabled for empty or underutilized nodes.
- NodeClass selects two private subnets in separate Availability Zones.
- All current workloads were placed on one node/AZ, so the application data plane is not highly available.

## Workloads

- ADOT Collector and Grafana were running.
- Retail UI, carts, catalog, checkout, and supporting database/message components were running.
- All inspected Pods were ready with zero observed restarts at discovery time.
- Application Services were internal `ClusterIP` Services.

## Networking

- VPC IPv4 CIDR observed: `10.0.0.0/16`.
- Kubernetes Service IPv4 CIDR observed: `172.20.0.0/16`.
- Nodes and Pods used VPC-native `10.0.x.x` addresses.
- Private subnets were tagged for internal ELB discovery.
- Only one public subnet was defined by Terraform.
- The public subnet did not have the Auto Mode public ELB discovery tag.
- NodeClass network-policy mode was default allow; network-policy event logs were disabled.

## Pod Identity

- Multiple EKS Pod Identity associations are managed by Terraform.
- The carts ServiceAccount is associated with a workload-specific IAM role.
- The role trusts `pods.eks.amazonaws.com` and permits role assumption/session tagging.
- Its policy is scoped to required DynamoDB actions and the carts table/indexes rather than a wildcard resource.

## Storage

- Default StorageClass uses Auto Mode EBS CSI: `ebs.csi.eks.amazonaws.com`.
- Volumes are encrypted GP3 with `WaitForFirstConsumer`.
- Expansion is allowed; reclaim policy is `Delete`.
- No PVCs or PVs existed at discovery time.
- A sample database StatefulSet used `emptyDir`; its data is therefore tied to Pod lifetime.
- A sensitive database value was present directly in a workload specification and should be externalized.

## kubectl compatibility

- Client version observed: `1.31`.
- Server version observed: `1.34`.
- This exceeds the supported one-minor version skew. Upgrade the client before administrative use.

## Load-balancer incident

The retail UI Ingress existed but had no load-balancer address after many hours. Kubernetes recorded the warning 157 times:

```text
Failed build model because automatic subnet discovery found fewer than the two required subnets.
```

Verified root cause:

1. The Ingress requests an internet-facing Auto Mode ALB.
2. Terraform creates only one public subnet.
3. ALB placement requires suitable public subnets in at least two AZs.
4. Public subnets must have `kubernetes.io/role/elb=1` for Auto Mode discovery.

No remediation was applied because adding subnets and creating an internet-facing ALB changes infrastructure, network exposure, and cost.

## Recommended order

1. Upgrade `kubectl`.
2. Decide between public and internal application exposure.
3. Correct subnet topology/tags in Terraform and review the plan.
4. Recreate the Ingress after approved subnet changes.
5. Add TLS and reduce inbound CIDRs.
6. Add replicas, disruption budgets, and topology spread.
7. Move databases to durable storage or managed data services.
8. Remove plaintext sensitive configuration.
9. Implement default-deny NetworkPolicies.
10. Restrict Kubernetes API public CIDRs or use private-only access where feasible.