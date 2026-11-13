# Assumptions and sources

Every number that appears in this model as a starting value is an assumption pulled from the Oats, Etc. repository, or it is an EXAMPLE ONLY figure. Nothing below is a measured cost, a confirmed fee, or a sales forecast. If a cost is not in the sources, it is left blank in the template.

File paths are relative to the root of `cwarloe/businessideas`. OE Growth Steward notes were read from pull request 3 (`notes/oe-challenger/`) and were not modified.

## Business and Stage 1 scope

Assumption: the Stage 1 offer is breakfast first, with one unsweetened cooked oatmeal base and a small set of toppings. Egg is excluded from the initial menu.

- Source: `docs/oats-and-more/research/decision-log.md` (entry menu row)
- Source: `docs/oats-and-more/research/pilot-and-equipment.md` (section "What are we actually selling?")
- Source: `docs/oats-and-more/README.md` (current pilot hypothesis)

Assumption: Stage 1 is a learning experiment around break-even, not a living-wage test. Gross sales are not profit. The operator is assumed to be a single person with no paid staff in these sketches.

- Source: `docs/oats-and-more/research/README.md` (operating principles: "Business quality matters more than volume")
- Source: `docs/oats-and-more/research/decision-log.md` (revenue lens row)
- Source: `notes/oe-challenger/adversarial-review-round-2-2026-11-11.md` (question: living, side income, or experiment you are happy to break even on)

Assumption: Charles does not yet have a building, a selected kitchen, or looked-up ingredient costs. Equipment, location, legal brand clearance, and licenses are not yet selected or approved.

- Source: `docs/oats-and-more/README.md`
- This is why the cost template is blank.

## Menu, proposed prices, and add-ons

These are proposed or illustrative prices, not tested prices and not measured willingness to pay. They are pre-filled on the menu-mix block so you can edit them. They are not copied into the average-ticket cell. You still choose a ticket or a mix.

Stage 1 starter menu (working price points from the research archive):

| Bowl | Proposed price | Source |
|---|---|---|
| Classic Brown Sugar and Cinnamon | $5.95 | `docs/oats-and-more/research/pilot-and-equipment.md` |
| Maple Walnut | $7.50 | same file |
| Apple Pie Oats | $7.95 | same file; apple handling and storage still subject to recipe and health review |

Suggested optional add-ons in that same file are labeled there as example upcharges, not verified demand or margins: cinnamon, brown sugar, and raisins +$0.75; walnuts or pecans +$1.50; maple/nut/crunch bundle +$2.00; extra oatmeal or large size +$2.00; shelf-stable drink +$2.00 to $3.00; a 10-bowl team pack with price still to be set.

The public concept site lists a broader menu and some different add-on prices, all labeled as test or illustrative prices. That site is not the Stage 1 pilot menu. It is recorded here so the two are not confused.

| Public-site item (not the Stage 1 default mix) | Listed price | Source |
|---|---|---|
| The Classic (cinnamon, brown sugar, butter) | $5.95 | `docs/oats-and-more/index.html`, `docs/oats-and-more/menu-board.html` |
| Apple Pie | $7.95 | same files |
| PB and Banana (overnight oats) | $7.95 | same files |
| Cheddar and Egg (grits) | $8.95 | same files |
| Mushroom and Herb | $9.95 | same files |
| Southwest Bowl (grits) | $10.50 | same files |
| Bowl-builder bases: warm oats, cheesy grits, overnight oats | $5.95, $6.95, $6.45 | `docs/oats-and-more/index.html` |
| Bowl-builder add-ons: apples, pecans, egg, cheese | +$1.25, +$1.50, +$1.75, +$1.00 | `docs/oats-and-more/index.html` |

The live flavor poll asks visitors which bowl they would try first and is not evidence of paid demand at a price, time, and place.

- Source: `integrations/oats-voting/README.md` (counts are directional market feedback, not verified people)
- Source: `docs/oats-and-more/research/validation-backlog.md` (same caution)
- Source: `notes/oe-challenger/adversarial-review-2026-11-11.md` (objection that the poll cannot produce demand evidence)

## Hours, volume hypotheses, and ticket used in archive models

Assumption, hours: the research describes a morning window of about 6:30 to 9:30 a.m., about three hours. This is a site hypothesis, not a confirmed host schedule. The service-hours cell in the template is left blank. If this window is the one you use, enter 3.

- Source: `docs/oats-and-more/research/decision-log.md`
- Source: `docs/oats-and-more/research/validation-backlog.md`
- Source: `docs/oats-and-more/research/local-regulation.md`

Assumption, days per week: not decided. The decision log lists 2, 3, 4, or 5 mornings as still open. The Stage 1 gross-sales table in the equipment memo uses 3 days per week as a model input, not a decision. The template leaves selling days blank.

- Source: `docs/oats-and-more/research/decision-log.md` (possibilities not decided)
- Source: `docs/oats-and-more/research/pilot-and-equipment.md` (Stage 1 table)

Assumption, volume: first test of 30 bowls before 9 a.m., and a working hypothesis of 30 to 60 paid bowls in the three-hour window. The Stage 1 table also uses 20 to 35 bowls per day as a model input. A later note says not to treat 30 as a hard ceiling if a large office site proves higher demand. All of these are hypotheses. None is filled in as a default forecast. You may type one into the optional "scenario bowls per day" cell to see profit at that volume.

- Source: `docs/oats-and-more/README.md`
- Source: `docs/oats-and-more/research/decision-log.md`
- Source: `docs/oats-and-more/research/pilot-and-equipment.md`
- Source: `docs/oats-and-more/research/validation-backlog.md`
- Source: `notes/oe-challenger/adversarial-review-round-2-2026-11-11.md` (the 30 to 60 figure has no headcount source)

Assumption, average ticket in the archive's Stage 1 gross-sales table: $7.50. The same file's three-hour sensitivity table also uses $9.00 and $10.50. The Challenger notes that an average of $7.50 is already at the Maple Walnut price and that an average above $7.95 needs add-ons, and that if everyone bought the $5.95 Classic with no add-on, Stage 1 gross would be lower. This model does not pre-fill $7.50 as your ticket. It is used only on the EXAMPLE ONLY sheet and as a cited figure in the sources.

- Source: `docs/oats-and-more/research/pilot-and-equipment.md`
- Source: `notes/oe-challenger/adversarial-review-round-2-2026-11-11.md` (objection 3)

Assumption, months: the archive converts weeks to months with a 4.33 multiplier. The workbook uses 4.33 as an editable assumption, with the same meaning: monthly figure = weekly figure times 4.33.

- Source: `docs/oats-and-more/research/pilot-and-equipment.md` (note under the three-stage table)

## Channels and selling models (qualitative only)

The research describes four lower-capital office breakfast channels: employer-paid catering, employee-paid preorder and pickup, a temporary indoor office breakfast counter, and a possible counter residency or revenue share. A hosted private commercial location with approved plug-in power is the current site hypothesis. These are planning options, not booked accounts. They do not change the formulas, but they can change which costs appear (for example a host fee, or kitchen hours without an on-site stand).

- Source: `docs/oats-and-more/research/boise-kitchen-and-office-service-market-2026-11-11.md`
- Source: `docs/oats-and-more/README.md`

## Kitchen rental, licenses, and other costs that exist only as research notes

Do not treat the following as filled-in model inputs. They are listed so you know where to look when you have a confirmed quote.

Advertised shared-kitchen hourly rates as of the November 11, 2026 research note, each labeled in that file as advertised prices to verify, not reservations: Gina's Kitchen $40 per hour; Flava Kitchen $30 per hour (booking page shows a 4-hour session); The Commons Federal Way $40 per hour prime and $20 per hour non-prime on a third-party listing; Osage Kitchen $35 per hour daytime and $25 per hour overnight on a third-party listing, with a two-hour minimum and a noted onboarding fee. Season and Taste requires a quote.

- Source: `docs/oats-and-more/research/boise-kitchen-and-office-service-market-2026-11-11.md`

That same file includes an illustrative gross-sales check that assumes a $9 average ticket and 2 kitchen hours per selling morning. Those two assumptions are used only on the EXAMPLE ONLY sheet, and only with this citation. Ingredient, packaging, fuel, licenses, and every other cost are excluded there, and they are excluded from that example here as well.

Published Central District Health example fees in the regulation memo: $100 plan review, and example full-service mobile license fees of $80 or $100 depending on category. The memo says to confirm fees and category at application, and that a portable stand may be classified differently.

- Source: `docs/oats-and-more/research/local-regulation.md`

Payment processing rates, insurance premiums, utility costs, fuel, spoilage rates, packaging prices, and ingredient prices are not in the repository as measured figures. They are left blank.

## Formulas (what the workbook computes, once you fill inputs)

These are definitions, not assumptions about values.

- Cost of one ingredient per bowl = purchase price divided by purchase quantity, times the amount used in one bowl. Use the same unit for purchase quantity and amount used.
- Bowl ingredient cost = shared oatmeal base cost + toppings for that bowl.
- Weighted ingredient cost = sum of (bowl ingredient cost times that bowl's share of sales). Shares should add to 100%.
- Packaging cost per bowl = sum of the same purchase-price method for cup, lid, spoon, napkin, and any other piece.
- Payment fee per bowl = (average ticket times card-fee percent) plus any per-transaction fee, times the share of bowls paid by card. If you leave these blank, they are treated as $0 and listed as omitted.
- Spoilage amount per bowl = ingredient cost times spoilage percent. Blank spoilage percent is treated as $0 and listed as omitted.
- Variable cost per bowl = ingredient cost + packaging + payment fee + spoilage + any other per-bowl cost you enter (for example a percent-of-sales host fee).
- Contribution per bowl = average ticket minus variable cost per bowl.
- Kitchen cost per selling day = hourly rate times hours reserved that day, using the larger of reserved hours and any minimum booking, if you enter a minimum.
- Weekly fixed cost = (per-day costs times selling days per week) + per-week costs + (per-month costs divided by 4.33, or whatever weeks-per-month value you enter) + (per-year costs divided by 52).
- Break-even bowls per week = weekly fixed cost divided by contribution per bowl. This is undefined if contribution is zero or negative, or if required inputs are missing.
- Break-even bowls per selling day = break-even bowls per week divided by selling days per week.
- Weekly gross at a scenario volume = average ticket times bowls per day times selling days per week.
- Weekly profit at a scenario volume (no operator wage) = contribution per bowl times bowls per week, minus weekly fixed cost.
- Profit per hour = weekly profit divided by weekly hours. Operator time is not treated as a cash wage in the primary break-even view.
- Monthly figures = weekly figures times weeks per month (default assumption 4.33).

The secondary income-target scenario uses the same costs. Bowls per week needed to hit a target cash amount = (weekly fixed cost + target weekly income) divided by contribution per bowl. That view is labeled as a scenario. It is not the Stage 1 goal.

Startup and one-time costs (equipment, deposits, onboarding, plan review) are listed separately. They are not included in weekly break-even unless you enter a recovery period in months. The archive's guidance is not to buy equipment until demand and a legal site are proven (`docs/oats-and-more/research/README.md`).

## What was deliberately not used

- No invented "typical" food-cost percentage.
- No invented payment-processor rate.
- No competitor prices or market size figures from outside the repository.
- No poll tallies as sales volume.
- No kitchen or permit research beyond what is already in the archive. Confirming a kitchen and a license path is other work.
- OE Growth Steward files under `notes/oe-challenger/` were read only.
