# AWS EKS Best Practices repository gap analysis

**Compared:** 2026-09-23 UTC  
**Upstream repository:** https://github.com/aws/aws-eks-best-practices  
**Upstream commit:** `45106f8c17914e0b2ffc2ea697c91717680ce189`  
**Method:** Shallow clone to a temporary directory; inventory of all AsciiDoc files/headings; detailed review of top-level indexes and key guidance. External text was treated as reference and not copied into this guide.

## Upstream inventory

The repository contained 477 files. Its current best-practice documentation covered:

- Security
- Reliability
- Auto Mode, Karpenter, and Cluster Autoscaler
- Networking
- Scalability
- Cluster upgrades
- Cluster version rollback
- Cost optimization
- Windows containers
- Hybrid deployments
- AI/ML workloads

Approximate source size for major domains:

| Domain | AsciiDoc files | Approximate characters |
|---|---:|---:|
| Security | 16 | 325,000 |
| AI/ML | 8 | 239,000 |
| Networking | 12 | 185,000 |
| Scalability | 10 | 157,000 |
| Cost | 8 | 152,000 |
| Windows | 15 | 107,000 |
| Reliability | 4 | 73,000 |
| Autoscaling | 4 | 63,000 |
| Hybrid | 6 | 46,000 |
| Upgrades | 1 | 45,000 |
| Rollback | 1 | 13,000 |

## Before-comparison coverage

The original local guide covered:

- EKS architecture and Auto Mode fundamentals
- kubectl, access entries, and RBAC
- basic VPC/Pod/Service/DNS networking
- Pod Identity
- EBS/PVC/PV fundamentals
- ALB/NLB exposure
- sanitized live-cluster audit
- introductory hands-on labs
- full explanation of the AWS “What is Amazon EKS?” overview

## Material gaps found

| Gap | Examples from upstream |
|---|---|
| Security depth | Pod security, policy as code, image/SBOM/signing, runtime, hosts, incidents, multi-tenancy, multi-account, SCPs, compliance |
| Application reliability | replicas, PDBs, topology spread, probes, graceful termination, rollout/rollback |
| Autoscaling | HPA/VPA relationship, Auto Mode/Karpenter/CAS design, Spot interruption, consolidation |
| Cluster scalability | API pressure, APF/429s, client caches, webhooks, CoreDNS, EndpointSlices, quotas, SLOs |
| Upgrade operations | deprecation inventory, insights, add-on sequencing, IP/IAM/KMS preflight, data-plane lifecycle |
| Native rollback | seven-day rollback window, readiness insights, node preparation, Auto Mode disruption, IaC timeouts |
| Cost optimization | allocation, right-sizing, purchase models, network/storage/observability cost loops |
| Advanced networking | prefix delegation, IPv6, custom networking, enhanced discovery, SG for Pods, conntrack/DNS, nftables |
| Hybrid behavior | WAN partitions, local dependencies, failover/split-brain, offline credentials |
| Windows | node scheduling/build compatibility, gMSA, hardening, patching, networking, memory, storage |
| AI/ML | accelerators, capacity, checkpointing, GPU sharing, EFA, model cache/storage, AI telemetry, CPU inference |

## Additions made

- `10-production-security.md`
- `11-reliability-autoscaling-scalability.md`
- `12-upgrades-and-rollback.md`
- `13-cost-and-performance-efficiency.md`
- `14-advanced-networking.md`
- `15-specialized-workloads.md`

Standalone diagrams added:

- `security-defense-in-depth.mmd`
- `scaling-loops.mmd`
- `upgrade-rollback.mmd`
- `cost-optimization-loop.mmd`
- `ip-capacity-planning.mmd`
- `hybrid-network-partition.mmd`
- `aiml-lifecycle.mmd`

## Deliberate scope boundaries

This local guide is a structured teaching companion, not a mirror of the upstream repository. It does not copy:

- upstream images or animations
- full command samples tied to standard EKS when they may not apply to Auto Mode
- third-party product lists
- example Gatekeeper/Kyverno/OPA policy repositories
- source prose
- binaries or project utilities

For implementation-level details, always follow the official AWS publication and current EKS/Kubernetes version documentation. Recommendations must be tested against the cluster operating model—especially Auto Mode versus standard EKS.

## Future refresh procedure

1. Fetch the latest upstream commit.
2. Compare `latest/bpg/**/*.adoc` headings against this matrix.
3. Review new/changed recommendations in the official AWS Docs publication.
4. Update original summaries and diagrams.
5. Validate links and sensitive identifiers.
6. Record the new upstream commit and review date.
