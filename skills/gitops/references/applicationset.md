# ApplicationSet lifecycle

An ApplicationSet owns its generated Applications. When a change stops generating a name (template `name` rename, removed list element, changed cluster label or selector) the old Application is deleted. Generated Applications carry `resources-finalizer.argocd.argoproj.io`, so deletion cascades to workloads and PVCs.

## Safe rename

1. Add to the ApplicationSet (not to the template's Application `syncPolicy`):

```yaml
spec:
  syncPolicy:
    preserveResourcesOnDeletion: true
```

2. Apply it, then check that the live Applications no longer have the finalizer.
3. Rename the template. The new Applications adopt the resources; keep `automated` with prune and selfHeal.

Do not add the finalizer to the template. Do not use `applicationsSync: create-only|create-update` as a rename workaround: it leaves two owners for the same resources.

## Templates

Go template syntax: `goTemplate: true`, `goTemplateOptions: ["missingkey=error"]`, `{{.cluster}}`.
