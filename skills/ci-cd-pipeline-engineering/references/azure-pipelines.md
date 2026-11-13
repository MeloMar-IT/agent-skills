# Azure Pipelines details

Docs: https://learn.microsoft.com/azure/devops/pipelines/

## Build once, promote by digest

```yaml
stages:
- stage: Build
  jobs:
  - job: BuildImage
    steps:
    - script: |
        # build and push once, capture digest into DIGEST
        echo "##vso[task.setvariable variable=digest;isOutput=true]$DIGEST"
      name: publish
- stage: Dev
  dependsOn: Build
  variables:
    imageDigest: $[ stageDependencies.Build.BuildImage.outputs['publish.digest'] ]
  jobs:
  - job: DeployDev
    steps:
    - script: ./deploy.sh dev $(registry)/$(image)@$(imageDigest)
- stage: Prod
  dependsOn: [Build, Dev]
  variables:
    imageDigest: $[ stageDependencies.Build.BuildImage.outputs['publish.digest'] ]
  jobs:
  - deployment: DeployProd
    environment: prod
    strategy:
      runOnce:
        deploy:
          steps:
          - checkout: self
          - script: ./deploy.sh prod $(registry)/$(image)@$(imageDigest)
```

`$(...)` is not evaluated for runtime output mapping; use `$[ ]`. Prod lists Build directly because `stageDependencies.Build` is invisible through Dev alone.

## Notes

- Environment approvals, checks and exclusive locks attach to the environment and trigger only for `deployment` jobs.
- Deployment jobs skip checkout; they auto-download pipeline artifacts.
- `Cache@2` key: `'"npm" | "$(Agent.OS)" | lockfile'` style, restore keys for fallbacks; not a way to pass build output.
- `extends:` a template to force required stages and block bypass of checks.
