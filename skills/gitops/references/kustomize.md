# kustomize in GitOps repos

- `replicas:` entries and patches also set `spec.replicas`. When a controller (HPA) owns replicas, remove it from the manifest, the `replicas:` block and patches.
- `commonLabels` also rewrites selectors, which are immutable on Deployments. Use `labels:` with `includeSelectors: false` for labels that must not reach selectors.
- `configMapGenerator` files go through Flux `postBuild` substitution like any rendered output.
- Render before review: `kustomize build <dir>` and diff against the live state.
