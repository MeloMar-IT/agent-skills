# Canary gate

- Error rate = errors / (requests - probes). Probes are synthetic checks, not users.
- `route_verdict(ce, cn, ke, kn)` takes user counts: canary errors, canary users, control errors, control users.
- FAIL when 95% confident the canary is worse than control by more than MARGIN; PASS when 95% confident it is not; otherwise INCONCLUSIVE.
- No canary user requests means INCONCLUSIVE.
- Canary and control traffic sizes differ.
- Release verdict: FAIL if any route FAILs, else INCONCLUSIVE if any route is INCONCLUSIVE, else PASS.
- The command line prints only the verdict word.
- Standard library only.
