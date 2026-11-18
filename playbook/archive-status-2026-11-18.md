# Businessideas archival inventory and gaps

**Audit date:** November 18, 2026  
**Checked:** GitHub default branch `main` tree through commit `22803d189bafc135d219dd22f36017d95ca2f1b9`, recent commits, branch list and open/closed PRs. This is a *repository state audit*, not access to every past chat or local/Drive document. Status may change; recheck before relying on it.

## What is where

| Workstream | Main-branch record at audit | Other location or limitation | Archival assessment |
|---|---|---|---|
| Oats, Etc. concept, design variations, website | [Project README](../docs/oats-and-more/README.md), homepage, design lab, menu board | Public Pages deployment can lag source/cache; check live URL | Substantial archive on main |
| Oats naming/trademark/taglines and pivots | [Research archive](../docs/oats-and-more/research/README.md), [decision log](../docs/oats-and-more/research/decision-log.md) | No completed legal name clearance | Saved, many questions open |
| Boise kitchens, office breakfast channels | [Market memo](../docs/oats-and-more/research/boise-kitchen-and-office-service-market-2026-11-11.md), [kitchen notes](../notes/oe-kitchen/README.md) | No kitchen or site reserved; prices researched on Nov 11 | Saved, leads to reconfirm |
| Food law, permits, compliance and scripts | [Local rules](../docs/oats-and-more/research/local-regulation.md), [back office](../notes/oe-back-office/start-here.md) | No regulator approval for proposed recurring private-office service | Saved, not approved |
| Sales/throughput/financial model | [Pilot and equipment](../docs/oats-and-more/research/pilot-and-equipment.md), [blank break-even workbook](../notes/oe-numbers/README.md) | Actual field sales and receipts absent | Model saved, economics not field validated |
| Challenges, mistakes and review | [Challenger round 1](../notes/oe-challenger/adversarial-review-2026-11-11.md), [round 2](../notes/oe-challenger/adversarial-review-round-2-2026-11-11.md) | No single portfolio-wide lessons document on main at audit | Partly archived; consolidated in this documentation PR |
| Cloudflare voting/D1/Worker | [Integration](../integrations/oats-voting/README.md) and source | Anonymous ballots only, not verified people; live service status is separate from code | Code and setup saved |
| Oats Pages static deployment verification | [Workflow](../.github/workflows/verify-live-site.yml) and [script](../.github/scripts/verify-live-site.sh), expanded November 18 | Read-only checks of served GitHub Pages files vs source; does not verify live Cloudflare/D1 logic | On `main`; operational lesson added to [retrospective](lessons-learned.md) in open PR #12 |
| Fudge sharing/gifting product, research and mockups | **Not on `main`** at audit | [PR #10](https://github.com/cwarloe/businessideas/pull/10) on `research/boise-fudge`, open/unmerged, 13 changed files, private preview; raw GitHub PR API later confirmed `mergeable: true` / `clean` | Preserved on branch, **not fully published to main** |
| Milk Bar specialty drinks + tasting concept | **Not on `main`** | [PR #14](https://github.com/cwarloe/businessideas/pull/14) holds dated decisions, customer experiences, profit risks and [research brief](https://github.com/cwarloe/businessideas/blob/research/milk-bar-concept-20261118/ideas/milk-bar/research-brief-v1.md) | Preserved for review; external research not started |
| Treasure Valley food gap / profitable-niche investigation | **No full results on main** at audit | [Research brief](../ideas/treasure-valley-food-gaps/README.md) reconstructs scope and prompt, but not the original completed results | Needs original findings or rerun |
| Reusable cross-product procedure and template | No consolidated version on main at audit | [Playbook](../BUSINESS_IDEA_PLAYBOOK.md), [template](new-idea-template.md) and [lessons](lessons-learned.md) added in a documentation PR | Prepared for review/merge |
| Older platform architecture / BBP concept | [Root README](../README.md) labels much of it a proposed scaffold | [PR #2](https://github.com/cwarloe/businessideas/pull/2) remains open | Do not mistake planned platform code for running infrastructure |

### Specific gaps not to conceal

1. **Fudge:** merge/rebase-review PR #10 before calling it published on main; check the live public path after merge. Do not discard the full research and images already in the PR.
2. **Milk Bar:** review and merge PR #14 when ready, then run the linked Round 1 research and commit sourced findings before calling market validation complete.
3. **Treasure Valley gap study:** retrieve the actual ChatGPT/Gemini result documents (if retained) or rerun the source-based prompt and save the sourced shortlist, rejected concepts and profit reasoning. This README only preserves the research *intent* and methodology.
4. **Chat provenance:** chat messages, attachments, local notes and external model outputs do **not** automatically enter GitHub. Statements like "everything from every chat is archived" are currently unverifiable.
5. **Oats validation:** paid demand, real ingredient receipts, a compliant host, specific health department classification, repeated sales, customer retention and finalized naming are still open; documentation must not imply execution.
6. **Current facts:** local food rules, shared-kitchen prices, trademark registrations and platform requirements require dated rechecks.

## Closeout procedure for future ideas

1. Review `main`, all open PRs and relevant branches; identify material changes not merged.
2. Compare with the current conversation's decision/assumption/asset list.
3. Preserve both positive and negative findings, source dates, rejected options, and corrections.
4. File new records against an idea folder using [the template](new-idea-template.md).
5. Open a PR, run link/content checks, merge after review and verify deployment where relevant.
6. In the session handoff, explicitly distinguish **merged**, **PR open**, **preview deployed**, **live** and **unknown**.

**Completion standard:** an indexed, reviewable `main` archive that someone can use to restart the idea without reconstructing the conversation. Until outstanding PRs and missing primary results are resolved, call this an **in-progress archive**, not a complete backup.
