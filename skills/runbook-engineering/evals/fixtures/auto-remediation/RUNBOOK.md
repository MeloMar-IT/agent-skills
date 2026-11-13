# Worker pods crash looping

Context `prod-eu-1`, namespace `jobs`. Workers carry the label `app=worker`.

## Step 1
Look at the pods.

    kubectl --context prod-eu-1 -n jobs get pods -l app=worker

## Step 2
Delete the worker pods that are in `CrashLoopBackOff` with a restart count of 5 or more. The deployment creates fresh replacements.

    kubectl --context prod-eu-1 -n jobs delete pod <name>

## Step 3
If pods keep crash looping after replacement, escalate to the `jobs-oncall` team.
