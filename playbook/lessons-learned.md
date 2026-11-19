# Lessons learned and mistakes to avoid — Oats, Etc. and portfolio work

**Captured:** November 18, 2026 · **Status:** retrospective of documented work and conversation decisions, **not** a claim that Oats, Etc. has operated or sold food.

This file preserves *why* the project changed direction. The source-of-record for the idea is [Oats research](../docs/oats-and-more/research/README.md), its [decision log](../docs/oats-and-more/research/decision-log.md), [first](../notes/oe-challenger/adversarial-review-2026-11-11.md) and [second](../notes/oe-challenger/adversarial-review-round-2-2026-11-11.md) adversarial reviews, [operating numbers](../notes/oe-numbers/README.md), and [permitting work](../notes/oe-kitchen/README.md).

## Mistakes, near-misses and better rules

| What happened / risk exposed | What we learned | Do differently next time |
|---|---|---|
| **The original Oats & More name had a potential trademark conflict.** Significant identity work existed before clearance. | Trademark, domain and common-law use are separate checks. An available URL is not permission to use a mark. | Run preliminary federal/state/common-law search before design; document serials, status and counsel questions. Keep names provisional until cleared. |
| **A liked tagline had prior promotional use.** "From the first bite to the last spoonful" was not reliably original. | A memorable phrase is not necessarily distinctive or protectable. | Verify exact/near-exact usage before calling copy original or exclusive. [Brand record](../docs/oats-and-more/research/brand-and-marketing.md). |
| **Brand studio and website polish arrived before paid-demand validation.** This made the concept look more advanced than the underlying evidence. | Beautiful prototypes are useful for presenting hypotheses, but can create sunk-cost attachment and false confidence. | Gate serious creative/technical investment behind customer/offer and economics checks; use simple low-cost tests first. |
| **The original equal breakfast/lunch vision expanded menus and operations.** Oatmeal, grits, savory lunch and eggs all compete for equipment and communication attention. | The simplest *pilot* need not be the entire eventual concept. Deferring lunch does not reject it. | Preserve the long-term concept, but test one familiar hero offer with few ingredients; keep expansion in a later-stage backlog. |
| **An e-bike/cart or attractive trailer threatened to determine the business model.** The 2017 Nissan Rogue's tow limit and complete wet-loaded weight became constraints. | Equipment is downstream of location, permit path and actual volume. Towing, tongue load and electrical supply need verified specifications. | Test the least-capital delivery format first (licensed kitchen + vehicle + hosted office/preorder where authorized); cost/measure every component before buying. [Equipment record](../docs/oats-and-more/research/pilot-and-equipment.md). |
| **Three 5-quart warmers and a 30–60-bowl morning sounded straightforward before peak-flow testing.** | Vessel volume, safe hot holding, serving size, warmup, refill, queue arrival waves and disposal all govern capacity. | Measure real per-serving yield and one-person throughput in an approved trial; do not turn rough arithmetic into a production guarantee. |
| **We initially considered sales volume more readily than margin.** The user asked specifically for sales-only projections, but gross revenue cannot answer whether the venture is worth doing. | Zero paid staff is not zero labor cost; operator hours and recurring prep/rental/insurance are economically real. | Maintain a gross-sales view *and* receipt-backed contribution, break-even, cash flow and owner-hour views. Unknown cells stay blank. [Model](../notes/oe-numbers/README.md). |
| **An anonymous "Which bowl?" poll was easy to deploy.** | One browser can vote more than once and choosing a free option is not willingness to pay. It cannot forecast volume. | Label poll as preference exploration; validate price with defined buyers, paid preorders and repeat purchases. [Voting caveats](../integrations/oats-voting/README.md). |
| **The proposed 30–60 bowls lacked an actual office traffic denominator.** | A target is meaningless without addressable headcount, conversion rate and repeat-frequency assumptions. | Count entrances/traffic, interview a defined buyer segment and verify host permission; calculate target orders from reachable people and expected purchase frequency. [Adversarial round 2](../notes/oe-challenger/adversarial-review-round-2-2026-11-11.md). |
| **Renting a commercial kitchen looked like a complete licensing solution.** | Permission to prepare does not automatically authorize transporting, hot-holding or selling at an office counter. Rules depend on the exact operation and location. | Describe the proposed service to the relevant health department *before* choosing equipment/commissary/host; preserve written responses and dates. [Local research](../docs/oats-and-more/research/local-regulation.md); [CDH call checklist](../notes/oe-kitchen/one-day-trial-checklist.md). |
| **A food-law change in March 2026 altered the research baseline.** | Using old "cottage food" assumptions can misclassify direct-serve food. The Oats documents distinguish a packaged product from a hot meal served immediately. | Start regulatory research with effective date, official statute and agency implementation; reverify before operating. This record reflects November 2026 research, not ongoing legal advice. |
| **The hosted-office model has two customers/gates:** workers who buy and property managers who allow service. | Product demand alone cannot create a viable site; an enthusiastic host alone cannot produce sales. | Validate host permission, power, access, promotion and site fee alongside employee price and repeat-demand tests. |
| **Technical prototypes mixed multiple publication states.** GitHub source, Pages output, design-studio preview, Worker/D1 deployment and domain/cache could appear out of sync. | A successful commit is not proof the public URL shows the change. | Log branch/commit/deployment URL; verify published version fingerprint, route, API health and live user flow after changes. |
| **GitHub Pages setup caused 404 confusion.** | Site assets, correct branch and `/docs` publishing path must agree, and Pages settings are per repository. | Record exact setup: Settings → Pages → Deploy from branch → main /docs (for this repo); validate root and subpath URLs. |
| **Research and prototypes were split among branches, PRs and live previews.** The fudge work was easy to overlook because it sits in open PR #10 rather than `main`. | Listing `main` files alone is an incomplete repository audit. | Check branches, PRs (including mergeability), asset previews, and default-branch tree before claiming "everything is published." |
| **Cross-chat results had no standardized end-of-session archival check.** The broader Treasure Valley food gap/profitability exploration was discussed but not documented on `main`. | Useful conclusions, rejected names and methodology can be lost even when site code persists. | At each session's end, update a dated decision log and source index, write negative results and open questions, and verify merge/deployment. |

## What worked especially well

1. **Adversarial review changed the operating concept.** It surfaced demand, menu, gross-vs-profit and siting assumptions rather than merely critiquing the copy. The feedback was saved in separate, dated files instead of erased.
2. **A staged pilot reduced downside.** The idea moved from a broad sweet/savory restaurant/trailer vision to one familiar breakfast offer at one hosted location, with later lunch expansion still possible.
3. **Separate research tracks created actionable artifacts.** Kitchen/permit scripts, a compliance register, a sourced market memo and a blank break-even workbook are more useful than a single optimistic narrative.
4. **Unknown values stayed unknown.** The spreadsheet asks Charles to supply real receipts and quotes. The archive calls 30–60 bowls a hypothesis, not a forecast.
5. **Technology was reused without sharing sensitive data.** The Oats poll reused the Charles Fan Club *pattern* but used a separate Cloudflare Worker and D1 database. Secrets were not committed to GitHub.
6. **Brand variants remained switchable.** The design lab allows testing names, layouts and language without constructing three independent production systems.

## November 18 follow-up: publishing verification became automated

After the earlier GitHub Pages/domain confusion, the repository added a source-to-live verification system: [deployment monitor workflow](../.github/workflows/verify-live-site.yml) (merged via [PR #13](https://github.com/cwarloe/businessideas/pull/13)) and [verification script](../.github/scripts/verify-live-site.sh), expanded on November 18 to cover the Oats homepage, design lab, public research page, menu board, vote-admin page and related JavaScript assets. The workflow runs after pushes to `main`, on a weekly schedule, and on demand; it retries while GitHub Pages propagates, then fails if served files don't match repository bytes.

**Reusable lesson:** A committed change, a successful CI build, and the bytes actually served by the public site are **different states**. Verify multiple user-facing entry points and assets, not just the homepage or a footer version number. Automate that comparison when the project grows, while keeping it read-only.

**Limit:** This monitor checks public static-file parity. It does **not** establish that Cloudflare Worker/D1 logic, authentication, poll integrity, real user flows or food-business field validation are correct. Those require separate targeted checks.

## Next-idea rules distilled

- Start with **customer pain, reachable buyers and profitable delivery**, not the logo, trailer or app.
- Write a *kill condition* and a cheaper alternative before every major expenditure.
- Separate **validated**, **sourced but not field-confirmed**, **estimated**, **hypothesized**, **rejected** and **deferred**.
- Record both successful and unsuccessful tests, including the counterfactual: *What would make us change our minds?*
- Reconcile **source branch → PR → merged main → live website/API** explicitly; don't say "published" merely because a preview exists.
- In any new chat, give the agent the idea brief and latest decision log. Before finishing, commit a short, dated handoff note.

## What is still *not* learned

There has been **no documented paid Oats field trial**, no verified office host contract, no completed regulator determination for the specific recurring office setup, no completed trademark clearance, and no real cost/retention dataset. Do not turn the above lessons into claims that a profitable operation has been proven.

## November 18 follow-up: keep the offer open until the evidence distinguishes it

- **The question drifted from “would someone buy milk?” to “would an oatmeal buyer add cocoa?”** The second model was useful for bundling. The customer, occasion and evidence needed for a milk stand or recurring milk order are different. Write those down before choosing what to cost or promote. [Milk Bar feasibility](https://github.com/cwarloe/businessideas/pull/16) · [Oats office comparison](https://github.com/cwarloe/businessideas/pull/17)
- **The selling format can drive earnings more than the product change.** In the Oats model, shortening service by using one employer delivery changed the modeled return per hour more than adding the drink to a staffed shift. Test the sales channel and count the whole job, from finding the buyer through cleanup. Actual route time, price and demand remain unverified. [Oats office comparison](https://github.com/cwarloe/businessideas/pull/17)
- **Founder flexibility is useful.** Agree on constraints first. Compare paid choices and repeat behavior before committing to a product format. Preserve the actual result and the options it leaves open in the next version of the [working business plan](business-plan-template.md).
