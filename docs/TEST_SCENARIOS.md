# Synthetic QA scenarios

Use fictional alerts and placeholder account identifiers only. These are test **cases to execute**, not claims that they already passed.

| Case | Synthetic input | Expected result |
| --- | --- | --- |
| Debit | UBA: debit NGN 4,500 for groceries, reference TEST-001 | One debit with a stable Event_ID |
| Credit | Wema: credit NGN 8,000, reference TEST-002 | One credit, excluded from expense totals |
| Duplicate | Deliver the same alert TEST-001 twice | A single ledger event after upsert |
| Internal transfer | UBA outgoing NGN 5,000 and OPay incoming NGN 5,000 with matching transfer context | Flag as potential own transfer; verify before excluding from spending |
| Ambiguous memo | OPay debit NGN 1,900, memo 'transfer' | Unknown category unless an explicit keyword rule matches |
| Failed parsing | Email with no amount or transaction reference | Preserve an exception rather than inventing values |
| Reporting | Multiple synthetic transactions across two dates | Daily and weekly summaries reconcile against the ledger |
| Budget threshold | Monthly sample spending crosses the configured 80% threshold | Expected warning delivered once according to workflow policy |

## How to run

1. Import the templates from `workflows/` into a test n8n instance.
2. Set up the Sheets tabs and OAuth permissions following the [README](../README.md).
3. Turn off external email notifications or point them to an authorized test inbox.
4. Run each synthetic case. Record input, expected output, actual output, execution ID and whether the test passed.
5. Reconcile the resulting ledger manually. Test separately for each bank's changing notification templates.

Never use real account identifiers or bank statements as public test fixtures.
