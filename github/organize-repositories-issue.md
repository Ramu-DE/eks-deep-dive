# Issue template: Organize EKS and container repositories

## Suggested title

```text
Standardize and catalog EKS and container repositories
```

## Suggested issue body

```markdown
## Goal

Create a consistent, discoverable portfolio for Amazon EKS, Kubernetes, container, and related AI/ML platform-engineering repositories.

## Tasks

- [ ] Review the proposed repository classification
- [ ] Apply common topics to confirmed EKS repositories
- [ ] Apply container/serverless topics to adjacent repositories
- [ ] Review `LLM-inference` for meaningful EKS content
- [ ] Review `Durable_AIOperations` and add a README if appropriate
- [ ] Add clear descriptions to repositories currently missing them
- [ ] Create an `eks-containers-hub` catalog repository
- [ ] Add repository maturity and maintenance status to the catalog
- [ ] Add architecture, prerequisites, license, and security sections to each README
- [ ] Cross-link related workshops and implementations
- [ ] Archive or clearly label abandoned experiments

## Topic baseline

Confirmed EKS repositories should normally include:

- `amazon-eks`
- `kubernetes`
- `containers`
- `aws`

Additional topics should reflect actual content, such as `eks-auto-mode`, `karpenter`, `gpu`, `llm-inference`, `platform-engineering`, `terraform`, `gitops`, `saas`, or `multi-tenancy`.

## Safety

- Do not place PATs, AWS credentials, kubeconfig files, Terraform state, account IDs, or unredacted command output in repositories or issues.
- Preserve existing topics when adding new topics.
- Review every public repository for accidental secrets before promoting it through the catalog.
```

## Where to create it

Preferred: the future `eks-containers-hub` repository. Until that exists, the profile repository `Ramu-DE/Ramu-DE` can hold the tracking issue if Issues are enabled.
