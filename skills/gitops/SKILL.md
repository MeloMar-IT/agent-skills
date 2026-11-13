---
name: gitops
version: 1.0.0
description: Keeps Argo CD and Flux GitOps repos from fighting other controllers or deleting live workloads, covering field ownership (HPA replicas, injected caBundle), ignoreDifferences, Flux drift detection, postBuild substitution and ApplicationSet renames. Use when an Argo CD Application or ApplicationSet, Flux Kustomization or HelmRelease, or kustomize file changes or drifts; not for CI promotion, canaries or incidents.
metadata:
  capabilities: [gitops, argocd, argo-cd, applicationset, flux, helmrelease, kustomize, ignore-differences, drift-detection, postbuild-substitution, sync-waves, resource-tracking]
  technologies: [argo-cd, flux, kustomize, helm, kubernetes]
---

# GitOps: Argo CD and Flux

Read the live behaviour first: who else writes this field, and what happens to the live resource when Git changes. Then make the smallest change that keeps self-heal, prune and auto-sync on for everything else.

## Decision rules

1. **Another controller owns a field** (HPA `replicas`, cainjector `caBundle`, operators, webhooks): give it to that controller in both places.
   - Argo CD: `ignoreDifferences` alone only hides the diff; sync and self-heal still write the Git value. Add `syncOptions: RespectIgnoreDifferences=true`.
   - Each entry needs `group` for non-core kinds (`apps`, `admissionregistration.k8s.io`), a `kind`, and a `name` when only some workloads are affected. A missing `group` means core and matches nothing.
   - List items: `jqPathExpressions: ['.webhooks[]?.clientConfig.caBundle']`, not `jsonPointers` with an index.
   - Remove the field from Git too (manifest, kustomize `replicas:`, patches, empty `caBundle: ""`). Do this together with `RespectIgnoreDifferences=true`, or the next client-side apply deletes the field and the workload drops to 1 replica.
   - Never ignore a whole kind, and never switch off selfHeal, prune or automated to stop one fight.
2. **Flux helm-controller**: keep `driftDetection.mode: enabled` and add `driftDetection.ignore` with `paths` and a `target` (kind and name). Never use `warn` or `disabled` to stop one fight; do not change chart version or remediation.
3. **Flux kustomize-controller** uses server-side apply: drop fields another controller owns from Git, check `managedFields` first.
4. **Flux `postBuild`** replaces every `${var}` in all rendered output, including `configMapGenerator` files, scripts and dashboards; unknown names become empty. Escape shell variables as `$${VAR}` or write `$VAR`. Keep Flux variables. Use `kustomize.toolkit.fluxcd.io/substitute: disabled` only on resources that need no Flux variable.
5. **ApplicationSet**: anything that stops generating an Application name (template rename, removed element, changed cluster label) deletes that Application, and its resources-finalizer deletes workloads and PVCs. Set `spec.syncPolicy.preserveResourcesOnDeletion: true` on the ApplicationSet (not in the template), roll it out first, check the live finalizers are gone, then rename. Never use `applicationsSync: create-only` as a rename workaround.
6. Pointers: sync waves are quoted strings; PreSync hooks use `BeforeHookCreation`; `Prune=false` and `Delete=false` protect single resources; `ServerSideApply=true` for oversized CRDs instead of `Replace=true`; kustomize `labels` with `includeSelectors: false` for labels that must not hit selectors.

## References

| Topic | File |
|-------|------|
| Argo CD ignoreDifferences, sync options, tracking | references/argocd.md |
| Flux helm-controller, kustomize-controller, postBuild | references/flux.md |
| ApplicationSet lifecycle and renames | references/applicationset.md |
| kustomize replicas, labels, patches | references/kustomize.md |
