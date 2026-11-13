# Readout and formulas

This is the short plain-language readout for the Stage 1 model. Calculated results appear in the workbook after you fill the yellow cells. Until then, the workbook should say "fill me in."

## Primary question

How many bowls do you need to sell, at the ticket and costs you entered, before the experiment covers its cash costs? After that, if you also enter a trial volume and your hours, what is left per hour of your time?

That is a break-even learning question. It is not "what salary does this pay."

## Formulas, written out

Let T be the average ticket in dollars per bowl.

Let V be variable cost per bowl: ingredients, plus packaging, plus any payment fee, spoilage, and other per-bowl amounts you entered.

Let C = T minus V. This is contribution per bowl.

Let F be weekly fixed cost, after converting per-day, per-month, and per-year amounts into a weekly figure. Kitchen rental is usually a per-day cost: hourly rate times hours reserved (or the kitchen's minimum, if larger).

Break-even bowls per week = F divided by C, but only if C is greater than zero and the required inputs are filled.

Break-even bowls per selling day = that weekly count divided by selling days per week.

Weekly profit at a scenario volume Q bowls per day, over D selling days = C times Q times D, minus F.

Profit per hour = weekly profit divided by weekly hours.

Monthly amounts = weekly amounts times weeks per month (the archive uses 4.33; that cell is editable).

Secondary income-target scenario, not the Stage 1 goal: bowls per week needed to leave a target cash amount I = (F + I) divided by C.

If T is at or below V, there is no break-even at that ticket. The workbook will say so instead of showing a huge or negative bowl count.

## What moves the answer most

Because C is the divisor, ticket and variable cost move break-even more than anything else when the margin is thin. A mix that leans on the $5.95 Classic, or an average ticket that assumed add-ons that customers do not buy, shrinks C. Kitchen rental is likely the largest repeating daily cost. Insurance and licenses hurt more per morning if you sell fewer days per week. Hours do not change break-even bowls. They change profit per hour.

## Required inputs versus omitted optional inputs

Required before the workbook will report break-even bowls:

- Average ticket, either typed in or computed from a complete mix.
- Ingredient cost, either by recipe (shared base plus toppings) or the blended shortcut.
- Packaging total per bowl (enter 0 if you truly have none).
- Selling days per week.
- Enough information to compute weekly fixed cost for the costs you want included. For kitchen rental, enter confirmed hours and a confirmed rate, or enter 0 if you are modeling a week with no kitchen charge.

Optional inputs (card fees, spoilage, host percent, utilities, and similar) are treated as $0 if left blank. The results sheet lists those omitted lines so the break-even figure is not mistaken for a complete cost picture.

## Example sheet

The workbook tab named `05_Example_only` walks through kitchen-only math using figures already published as illustrations in the research archive. It does not invent ingredient or packaging costs, so it is a floor, not a complete break-even. See that tab's labels and `assumptions-and-sources.md`.
