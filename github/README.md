# GitHub EKS and Containers Repository Catalog

**Owner:** [Ramu-DE](https://github.com/Ramu-DE)  
**Discovery:** Public repository metadata and public README files, 2026-09-23.  
**Security:** No GitHub token was used. The PAT shared in chat must be revoked and is intentionally absent from every file and command.

## Recommended organization model

Use all three layers:

1. **Repository topics** make each project discoverable and consistently categorized.
2. **A catalog repository** such as `eks-containers-hub` provides one curated landing page with categories, maturity, architecture, and links.
3. **An issue** tracks cleanup work. An issue by itself does not group repositories.

A GitHub organization is a later option if these projects need shared teams, permissions, policies, or a separate namespace. Moving repositories is a larger governance change and is not required merely to create a portfolio collection.

## Confirmed Amazon EKS repositories

| Repository | Focus | Suggested primary group |
|---|---|---|
| [Customizing-LLMs-on-AWS-EKS](https://github.com/Ramu-DE/Customizing-LLMs-on-AWS-EKS) | GPU-based LLM deployment and customization on EKS | EKS AI/ML |
| [Building-production-ready-AI-Agents-on-Amazon-EKS](https://github.com/Ramu-DE/Building-production-ready-AI-Agents-on-Amazon-EKS) | Production AI agents on EKS Auto Mode | EKS AI/ML |
| [SaaS-platforms-using-Amazon-EKS-Auto-Mode-](https://github.com/Ramu-DE/SaaS-platforms-using-Amazon-EKS-Auto-Mode-) | Multi-tenant SaaS with Auto Mode, Argo CD, ACK, and kro | EKS platform/SaaS |
| [Platform_EKS](https://github.com/Ramu-DE/Platform_EKS) | Platform engineering, Terraform, IAM, networking, and ECR on EKS | EKS platform engineering |
| [Secure-AI-Agents-on-AWS_EKS](https://github.com/Ramu-DE/Secure-AI-Agents-on-AWS_EKS) | Secure AI-agent workloads on EKS | EKS security/AI |
| [Optimize--Inference-EKS](https://github.com/Ramu-DE/Optimize--Inference-EKS) | GPU inference optimization on EKS Auto Mode | EKS AI/ML performance |

## Confirmed container-adjacent repositories

| Repository | Focus | Why it is separate from EKS |
|---|---|---|
| [Migration-Modernization_Containes](https://github.com/Ramu-DE/Migration-Modernization_Containes) | Container migration and modernization | Public README unavailable; EKS usage is not yet confirmed |
| [Run-AI-agent-generated-code-securely](https://github.com/Ramu-DE/Run-AI-agent-generated-code-securely) | Lambda container images and Firecracker MicroVM isolation | Containers/serverless, explicitly not an EKS workload guide |

## Candidates requiring manual review

| Repository | Reason |
|---|---|
| [LLM-inference](https://github.com/Ramu-DE/LLM-inference) | General production inference content; public README did not establish EKS scope |
| [Durable_AIOperations](https://github.com/Ramu-DE/Durable_AIOperations) | Public README unavailable |

Do not add `amazon-eks` merely because a project runs AI software or uses containers. Topics should describe substantial repository content.

## Topic taxonomy

### Common EKS topics

```text
amazon-eks
kubernetes
containers
aws
```

Add only when applicable:

```text
eks-auto-mode
karpenter
terraform
gitops
platform-engineering
workshop
```

### AI/ML on EKS

```text
ai-agents
llm
llm-inference
gpu
machine-learning
model-serving
performance-optimization
```

### Platform and SaaS

```text
saas
multi-tenancy
argo-cd
ack
kro
pod-identity
observability
```

### Container-adjacent

```text
containerization
migration
modernization
aws-lambda
serverless
firecracker
microvm
```

GitHub limits repository topics, so prefer a focused set rather than attaching every possible keyword.

## Proposed catalog repository

Recommended name:

```text
eks-containers-hub
```

Recommended description:

```text
Curated catalog of Amazon EKS, Kubernetes, containers, and AI/ML platform engineering projects.
```

Recommended topics:

```text
amazon-eks kubernetes containers aws platform-engineering portfolio
```

The catalog README can reuse the tables in this file and later add:

- project maturity: concept, workshop, reference architecture, production candidate
- architecture diagram
- primary AWS services
- prerequisites
- maintenance status
- license
- security considerations

## Safe application workflow

1. Revoke the PAT exposed in chat.
2. Create a new fine-grained credential with only required repository permissions.
3. Keep the credential outside files and command history.
4. Run the topic script in dry-run mode.
5. Review additions and repositories skipped.
6. Run with `--apply` only after approval.
7. Create the catalog repository separately.
8. Open the prepared tracking issue in the catalog or profile repository.
