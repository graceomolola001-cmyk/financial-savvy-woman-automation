# Financial Savvy Woman

Reusable, privacy-conscious **n8n + Gmail + Google Sheets** personal finance automation.

## Why this project exists

A bank-alert inbox can contain hundreds of entries spread across multiple institutions. Each alert must be interpreted, checked for duplicates and matched to transfers before the figures become useful. This project explores that workflow with reusable n8n templates and a Google Sheets ledger.

**Scenario:** A user receives a UBA debit alert, moves money to OPay, and later receives a Wema notification. A naive tracker counts both sides of an own-account transfer as spending. This workflow applies deterministic parsing, event IDs and cautious transfer matching, retaining unknown items for reconciliation.

**What you can reproduce:** import the two templates, configure OAuth credentials privately, set up the four documented Sheets tabs, submit synthetic alerts, and inspect entries and summaries. Do not assume the templates have production-level accuracy without testing each bank's actual alert formats.

**Portfolio scope:** reusable implementation and demonstration. No verified savings, transaction count, or production uptime is claimed.

See [synthetic test scenarios](docs/TEST_SCENARIOS.md) for a repeatable QA checklist.

## What it does
- Parse UBA, OPay and Wema bank-alert messages into credit/debit ledger entries.
- Categorise **debits** from explicit transfer narrations using editable keyword rules.
- Leave unclear or ambiguous purposes as **Unknown**, rather than inventing spending categories.
- Find likely transfers between own accounts without silently treating every matching amount as an internal transfer.
- Upsert by **Event_ID** to reduce duplicate alerts.
- Produce daily summaries, Sunday weekly recaps and configurable budget threshold warnings (default 80%).

## Repository contents

- `workflows/bank-alerts.template.json`: **sanitised** transaction automation template.
- `workflows/daily-weekly-budget-alerts.template.json`: **sanitised** reporting template.
- `scripts/check_public_export.py`: automated scan for common sensitive patterns.
- `.env.example`: placeholder names only; no live configuration.
- `.gitignore`: excludes local exports, statements, transactions and credentials.

## Security and privacy

This repository is **public**. The templates contain no connected OAuth credential assignments, banking transaction histories, actual bank balances, personal email addresses, live spreadsheet IDs, or live n8n instance URLs. Placeholder values such as `REPLACE_WITH_SPREADSHEET_ID` must be configured **privately** after import.

**Do not upload:** raw n8n workflow exports, credential backups, OAuth tokens, bank statements, email messages, account numbers, phone numbers, names, private transaction spreadsheets, n8n execution data or personal budget figures.

`.gitignore` only protects untracked files. If sensitive data is committed accidentally, deleting it in a later commit is not enough. Rotate compromised credentials and purge the public Git history.

## Import and configure

1. Import each `workflows/*.template.json` into your n8n installation.
2. Assign your own Gmail OAuth2 and Google Sheets OAuth2 credentials **inside n8n**.
3. Replace `REPLACE_WITH_SPREADSHEET_ID` in each Google Sheets node with the actual Google Sheet ID, **inside n8n only**.
4. Provide Google Sheets tabs named `Transactions`, `Parser Exceptions`, `Categories & Rules` and `Alert Settings`.
5. Set up your own authenticated webhook path or disable the optional mobile webhook trigger.
6. Populate `Categories & Rules` with `Expense category`, `Keywords / description`, and `Monthly budget (₦)`. Separate keyword phrases with `|`.
7. Populate `Alert Settings` with `Setting` and `Value` columns, including `Report email`, `Daily email enabled`, `Sunday weekly recap enabled`, `Overall monthly spending limit (₦)`, and `Warn at percentage of budget`. The reporting template expects its headers on **row 3**.
8. Set the n8n reporting workflow's timezone to `Africa/Lagos`; reconnect the Gmail sending node and perform tests with **synthetic transactions** before activating.
9. Verify deduplication, bank-specific parsing, matching of own transfers and the actual account statement balances before relying on financial results.

The templates are examples that require private credentials and configuration. The real user's deployed n8n instance and financial spreadsheet are not stored here.

## Before each commit

```bash
python scripts/check_public_export.py
```

Then manually inspect changes to workflow Code nodes, webhook paths, node parameters and the full diff for private details. Automated scanning is helpful, but cannot guarantee that all secrets have been detected.

## Financial accuracy

Bank-alert coverage may be incomplete, especially when banks use other notification channels. A successfully parsed debit is not necessarily a verified expense. Account movements do not constitute a formal accounting balance sheet. Reconcile with bank statements to establish actual balances.
