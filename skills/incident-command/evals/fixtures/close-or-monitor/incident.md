# INC-2291 Duplicate invoices

invoice-batch is a Kubernetes CronJob `invoice-nightly`, schedule "0 2 * * *", timeZone "Europe/Amsterdam"; a run takes 20 to 25 minutes.
The run of the night of 11 to 12 Nov e-mailed 1,240 customers a second invoice.

Log (UTC, 2026-11-12):
- 07:10Z support reports duplicates
- 07:25Z declared SEV2, IC Ana Silva
- 08:05Z feature flag `invoice_autosend` set to false (invoices are generated but not e-mailed)
- 08:10Z alert `InvoiceDuplicates` silenced until 2026-11-15T00:00Z because it kept firing on old rows
- 11:30Z Carlos Mendes voided the duplicates
- 15:40Z fix deployed: an idempotency key per customer and billing period (PR 812, Dev Patel)
- 16:20Z no new duplicate rows; the batch has not run since the fix

Now: 2026-11-12 16:30Z.
People: Ana Silva (IC), Dev Patel (owns invoice-batch), Carlos Mendes (billing), Omar Haddad (on call tonight).
