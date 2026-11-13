# Flux

## helm-controller drift detection (`helm.toolkit.fluxcd.io/v2`)

```yaml
spec:
  driftDetection:
    mode: enabled        # enabled | warn | disabled
    ignore:
      - paths: ["/spec/replicas"]
        target:
          kind: Deployment
          name: api
```

Use `ignore` for the one field. Do not move to `warn` or `disabled`, do not change chart version or remediation, and do not raise `replicaCount` to hide the fight.

## kustomize-controller

Applies with server-side apply. Remove fields other controllers own from Git; inspect `managedFields` to see the owner. `kustomize.toolkit.fluxcd.io/ssa: IfNotPresent` applies a resource only once; `kustomize.toolkit.fluxcd.io/prune: disabled` keeps it on removal from Git.

## postBuild substitution

- Every `${var}` in the rendered output is replaced, including `configMapGenerator` files, scripts and dashboards. Unknown variables become empty strings (unless `StrictPostBuildSubstitutions` is on), which is how `${DATABASE_URL}` in a script turns into nothing.
- Escape shell variables: `$${VAR}` (rendered as `${VAR}`), or write `$VAR` without braces.
- `kustomize.toolkit.fluxcd.io/substitute: disabled` switches off substitution for a resource; use it only when that resource needs no Flux variable.
- Variable names match `^[_[:alpha:]][_[:alpha:][:digit:]]*$`. Defaults: `${var:=default}`.
