example-api 4.x always renders `replicas: {{ .Values.replicaCount }}`; it has no autoscaling switch; it is a vendor chart we cannot fork.

It renders two Deployments: `api` with `replicas: {{ .Values.replicaCount }}` and `api-worker` with `replicas: {{ .Values.workerReplicas }}`. Only `api` has an HPA.
