# Milk Bar — Three independent website prototypes

**Prepared:** 2026-11-18 · **Status:** review branch; not published, not market validation.

[Open the interactive picker](index.html) when previewing the branch locally. Switch between **The Milk Atlas** (discovery), **Velvet Milk** (indulgent signatures) and **Good Milk Co.** (everyday convenience) with the fixed top picker. Use **Compare concepts** for their separate strengths and failure modes. The picker persists the choice locally and supports direct hashes: `#discovery`, `#signature`, `#everyday`.

These are **independent creative strategies**, not three palette swaps: distinct copy, visual identities, customer occasions, ordering hierarchy, signature menus, and calls to action. All three preserve the same underlying quick-service + 2–4-person tasting-ledge concept and the balance of milk-forward and signature drinks.

## Preview without publishing

Download or clone this feature branch, then open `docs/milk-bar/index.html` in a browser. The prototype is standalone HTML/CSS/JS with no build step or backend. Google Fonts are optional: fallback fonts work offline. It contains no checkout, email capture, analytics, or real ordering.

**Important:** GitHub Pages currently serves `main/docs`; this branch is **not** the live public website. Do not merge or deploy until Charles reviews. To compare on a phone, use a branch-capable preview environment or download the HTML file and open it locally.

## Critique / decision

| Direction | Positioning advantage | Adversarial concern | Cheapest decisive test |
|---|---|---|---|
| Milk Atlas | A differentiated tasting story | Novelty visitors may not repeat | Sell flights at approved pilot, track follow-on paid drinks |
| Velvet Milk | Craveable repeat-use drink story | Strong boba/smoothie/dessert substitutes | Paid signature-drink orders on comparable exposure |
| Good Milk Co. | Quick, familiar, low-friction | Ordinary milk may not justify premium | Test paid price acceptance and repeat at hosted site |

**Do not select a winner by aesthetics.** Test both discovery-led and signature-led messages under comparable conditions; treat the everyday variant as a third framing hypothesis.

## Scope and limits

- No product photography, real product prices, ingredient/supplier commitments, cleared brand names or permission to serve.
- No verified sales, demand, margin or repeat rate. Brand names are provisional.
- Accessible buttons, mobile responsive layout, reduced-motion support, semantic sections, no data capture.
- The prototype is for concept review. [Operating and Idaho compliance notes](operations-idaho.md) are a separate internal learning document, not consumer-facing copy.
- Canonical concept: [idea record](../../ideas/milk-bar/README.md); [research brief](../../ideas/milk-bar/research-brief-v1.md).

## Review checklist

1. Open all three designs on desktop and phone; use picker and comparison.
2. Check navigation anchors, responsive wrapping, keyboard focus, and no broken scripts.
3. Assess whether customer promise is clear in five seconds and each offer has a distinct reason to return.
4. Do **not** infer feasibility from visual appeal. Validate with paid behavior and measured owner-hour economics.

## Handoff

Branch: `feature/milk-bar-three-prototypes-20261118`. This is a reviewable checkpoint, not merged. Next: visual QA in real browsers; gather Charles's preference; complete separately sourced Round 1 market/competitor study; use findings to revise copy and decide what to test. Then model actual quoted costs and regulatory requirements before any sales pilot.
