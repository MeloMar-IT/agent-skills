# Argo CD field ownership

## HPA-owned replicas (one Deployment)

```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      name: checkout
      jsonPointers:
        - /spec/replicas
  syncPolicy:
    automated: {prune: true, selfHeal: true}
    syncOptions:
      - RespectIgnoreDifferences=true
```

Then remove `spec.replicas` for that workload from the manifest, from kustomize `replicas:` and from patches. Other workloads keep their Git replica count.

`RespectIgnoreDifferences=true` only affects resources that already exist. Without it (or server-side apply), removing `replicas` from Git makes a client-side apply delete the field once and the Deployment falls to 1 replica.

## Injected fields (cert-manager caBundle)

```yaml
ignoreDifferences:
  - group: admissionregistration.k8s.io
    kind: MutatingWebhookConfiguration
    jqPathExpressions:
      - '.webhooks[]?.clientConfig.caBundle'
  - group: admissionregistration.k8s.io
    kind: ValidatingWebhookConfiguration
    jqPathExpressions:
      - '.webhooks[]?.clientConfig.caBundle'
```

Plus `RespectIgnoreDifferences=true`. Remove `caBundle: ""` placeholders from Git. `jsonPointers` cannot wildcard list items; `managedFieldsManagers` is an alternative.

## Other options

- Waves: `argocd.argoproj.io/sync-wave: "5"` (quoted).
- Hooks: `argocd.argoproj.io/hook: PreSync` with `hook-delete-policy: BeforeHookCreation`.
- `argocd.argoproj.io/sync-options: Prune=false` or `Delete=false` on a resource.
- Oversized CRDs: `ServerSideApply=true`, not `Replace=true`.
- Tracking: annotation tracking is the default since Argo CD 3.0; label tracking clashes with Helm `app.kubernetes.io/instance`.
