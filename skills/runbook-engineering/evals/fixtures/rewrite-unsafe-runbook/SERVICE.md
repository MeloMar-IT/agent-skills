# payments-api

- Kubernetes context: `prod-eu-1`
- Namespace: `payments`
- Deployment: `payments-api`, pod label `app=payments-api`
- Normal replicas: 6
- PodDisruptionBudget: `maxUnavailable: 1`
- Escalation: team `payments-oncall`
