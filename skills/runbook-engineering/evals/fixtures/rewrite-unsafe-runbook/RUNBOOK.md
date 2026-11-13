# Payments API is failing

1. Switch to prod:

        kubectl config use-context prod-eu-1

2. Find the pods:

        kubectl get pods -A | grep payments

3. Reset everything and scale back up:

        kubectl delete pods --all -n payments && kubectl scale deploy payments-api -n payments --replicas=6

4. Check the logs, should be fine.
