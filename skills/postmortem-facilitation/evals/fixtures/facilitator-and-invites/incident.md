# INC-2041 Payment failures at checkout (SEV2)

Affected services: checkout-api, payments-gateway. Contributing services: orders-db (connection pool exhaustion), ledger-sync (stale reference data).

Timeline (UTC):
- 08:55 Ben Okafor deployed a checkout-api change lowering the client retry timeout
- 09:12 Dev Patel escalated customer reports of failed payments
- 09:14 Omar Haddad acknowledged the page and escalated to Ana Silva
- 09:20 Carlos Mendes took the incident commander role
- 09:31 Ana Silva shifted payments traffic to region B; errors continued
- 09:35 Lea Park joined the channel and asked for an ETA
- 09:40 Wei Zhang raised the orders-db connection pool limit; errors halved
- 09:52 Ben Okafor reverted the retry change after Carlos Mendes asked for recent deploys; errors stopped
- 10:05 Carlos Mendes declared the incident mitigated
