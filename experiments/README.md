# Lean experiment traveler (internal work record)

This is a **measurement and handoff aid** for the existing [Business Idea Playbook](../BUSINESS_IDEA_PLAYBOOK.md), not a replacement for its eight stages, the decision-history source of truth, or the proposed broader [PR #18](https://github.com/cwarloe/businessideas/pull/18). The GitHub Pages site is served from `/docs`; this folder contains internal, generic working files. Note that **the repository itself is public**.

## One experiment, one traveler

1. Begin with a hypothesis/experiment event in [`docs/data/decision-history.json`](../docs/data/decision-history.json), linked to real original research. No event? Propose one for owner review; don't invent a completed test.
2. Copy [`_template.json`](_template.json) to `<unique-id>.json`, fill `idea` with the canonical idea ID and `history_event_id` with the matching event. The underscore-prefixed template is intentionally excluded from actual metrics.
3. Before any real action, specify exactly who counts as a buyer, the test, sample denominator, threshold, cash/time caps and known limitations. Commit this plan first. Git history is the audit trail; **the validator cannot prove a plan was registered before a field test**.
4. Keep state `PLANNED` and authorization `NOT_APPROVED` until Charles explicitly authorizes an experiment. Recording an approval is not a mechanism for obtaining it. No outreach, payments, filings, purchases or field tests are authorized by this format.
5. With separate authority, record `RUNNING`, then `COMPLETED` with dated, source-backed **aggregates only**. Keep unknown spend and owner-hours as `null`, not zero. Never commit names, raw interview quotes, emails, payment records, customer lists, children’s identifiers or confidential supplier material.
6. The validator compares the observed success proportion to the *predeclared* rate when the sample minimum is met. That is **not** proof of demand, profitable unit economics, statistical significance, or an automatic choice to proceed. Charles's recorded `owner_decision` remains separate.
7. On cancellation, write `CANCELLED` and explain why. Preserve failed experiments and countermeasures rather than deleting them. Update the decision-history event only after reviewing the evidence and making the appropriate owner decision.

## Checks

Run `node scripts/validate-experiments.mjs` and `node --test scripts/test-validate-experiments.mjs`. Both run in existing GitHub Actions decision-history validation. The report is factual: with no experiment records, `records: 0`, `threshold_attainment_rate: null`, and `total_spent_usd: null`. The threshold-attainment metric is only the fraction of evaluable experiments that met their *own registered threshold*. It is **not first-pass yield** (rework has not been measured), business success or evidence of profitable demand.

The validator rejects malformed records, impossible dates/counts, unlinked idea hypotheses, invented execution on `PLANNED` entries, completion without observed evidence, unapproved execution, and implicit owner decisions. It *alerts* rather than hiding an actual budget/time overrun. It cannot prove a source is genuine, an approver is authentic, or a past Git commit actually predates a field observation; peer review must inspect those claims.

### Stop-the-line triggers

- Missing approval to perform real customer or spending activity.
- Incomplete, contradictory or private/sensitive evidence.
- Missing denominator, unknown economics, or a sample below the planned minimum.
- Actual spend or owner-time beyond recorded caps.
- An attempt to label preferences, votes, or mockup interactions as paid purchases.

The appropriate next step is correction, a narrower experiment, or an owner decision, not an automatic retry that incurs new cost.
