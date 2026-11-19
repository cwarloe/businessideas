# Decision history: shared format and publishing rules

This is a **public, read-only history** of the business-idea process, not a live sales dashboard or a replacement for the original research. The canonical structured record is [`docs/data/decision-history.json`](../docs/data/decision-history.json). The browsable view is [`docs/decision-history.html`](../docs/decision-history.html), served through the existing GitHub Pages `/docs` directory. GitHub commits and pull requests provide review history.

## What belongs here

Record decisions, testable assumptions, proposed experiments, sourced findings and reusable lessons. Keep the distinction between a suggestion, Charles's preferred direction, a validated finding and an executed test. Record **negative results and rejected options** as carefully as positive ones. A poll preference is not proof of purchase intent.

Each event has:

| Field | Meaning |
| --- | --- |
| `id` | Stable, unique identifier, e.g. `oats-etc-2026-11-18-01` |
| `date` | Date the original decision or observation was recorded, `YYYY-MM-DD`; not the date someone later digitized it |
| `idea` | Slug in the top-level `ideas` list |
| `kind` | `decision`, `hypothesis`, `experiment`, `finding` or `lesson` |
| `status` | The degree of commitment or evidence; see allowed values in the validator |
| `title`, `summary` | Plain-language explanation, without presenting assumptions as facts |
| `why` | Rationale or significance of the evidence |
| `revisitWhen` | A specific trigger to reverse, revise or follow up; may be `null` only when not applicable |
| `sources` | At least one linked primary research/decision file or dated external evidence source |
| `supersedes` | Optional ID of an earlier event this one corrects or replaces |

For repository evidence use `{ "path": "ideas/milk-bar/README.md", "label": "Milk Bar record" }`; for an external source use `{ "url": "https://example.com/report", "label": "Report, checked 2026-11-18" }`. External facts should include their date and caveat in the underlying research. Do not insert unverifiable source links.

## Record a new decision

1. Update the idea's original research or decision notes and commit the supporting evidence.
2. Append an event to `docs/data/decision-history.json`, with a new ID and source link. Mark untested, provisional, proposed or open work honestly.
3. **Do not rewrite old decisions to make the history look cleaner.** Add a new dated event with `supersedes` when an earlier assumption or decision changes. Preserve the previous event as historical context.
4. Run `node scripts/validate-decision-history.mjs` locally, or let the GitHub Actions check run on the pull request.
5. Merge after reviewing both the structured history and its source documents. The Pages timeline will update with GitHub Pages deployment.

## Public-content boundary

This repository and GitHub Pages site are public. Do not publish personal phone numbers, private customer interview details, supplier quotes under NDA, Cloudflare credentials, ballot tokens, email addresses, payment data, or identifying information about minors. Use anonymized summaries with permission or keep sensitive materials outside this public repository. The timeline does **not** access Cloudflare D1 or expose the Oats voting API.

## Initial import limitation

The first dataset transcribes selected events from the existing Oats, Fudge and Milk Bar records. It is **not** a complete reconstruction of every chat or field result. Source documents remain authoritative where more detail is needed. New research may add events, but must not silently upgrade a proposed experiment into a completed one.
