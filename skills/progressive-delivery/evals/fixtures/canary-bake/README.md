# Canary steps

- A step is promoted only when `verdict` over the step's analysed requests is PASS.
- Routes are gated separately: a step is promoted only when every route passes, so a small route is not hidden by the others. `route_share` in `traffic.json` is each route's share of the traffic.
- `decide(checkpoints, bake_minutes, extended=False)` is called every minute. `checkpoints` maps a minute to `{route: (errors, requests)}`, the cumulative counts since the step started, for every minute from 1 up to now; `bake_minutes` is the planned bake; `extended` is True once this step's bake was already extended. It returns one of: `"promote"` (go to the next step), `"wait"` (keep baking), `"extend"` (add bake time to this step), `"hold"` (stop the rollout at this weight and page the owner), `"rollback"` (send the canary traffic back to the old version).
- Limit: 0.1% of user requests, 95% confidence.
- FAIL only when 95% confident the rate is above the limit.
- 0 requests means INCONCLUSIVE.
- The first 5 minutes of a step are warm-up and are not analysed.
- Each canary step bakes at least 10 minutes.
- The final step (weight 1.0) has `bake_minutes` 0.
- No step bakes more than 5 minutes longer than a healthy, zero-error canary needs to PASS on every route.
- `requests_per_minute` is the whole fleet; a step with weight w sends `w` of it to the canary.

Incident note: a release with a 0.4% error regression passed the 1% step after a few hundred requests.
