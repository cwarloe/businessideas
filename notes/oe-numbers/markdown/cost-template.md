# Stage 1 cost template (Charles fills this in)

Print this, or paste the tables into Excel or Google Sheets. Yellow-equivalent meaning: every empty amount cell is yours to fill from a receipt or a quote. Do not guess. If a cost does not apply, enter 0 once you are sure. The live formulas live in `oats-etc-stage1-breakeven.xlsx`, not in these tables.

Proposed bowl names and prices below are assumptions from `docs/oats-and-more/research/pilot-and-equipment.md`. Change them if your menu changes.

## 1. Operations

| Input | Value (CHARLES FILLS THIS IN) | Unit | Notes |
|---|---|---|---|
| Selling days per week |  | days | Not decided in the archive (2, 3, 4, or 5). See `decision-log.md`. |
| Serving window |  | hours per selling day | Archive hypothesis is about 6:30 to 9:30 a.m. (3 hours). Enter 3 only if that is your window. |
| Weeks per month | 4.33 | weeks | ASSUMPTION copied from the monthly math in `pilot-and-equipment.md`. Edit if you prefer another convention. |
| Scenario bowls sold per selling day (optional) |  | bowls | Optional. Used only to show profit at a volume you choose. Not a forecast. Archive hypotheses of 20 to 35 (Stage 1 table) or 30 to 60 (working hypothesis) may be typed here as a scenario if you want to inspect them. |
| Manual average ticket (use if you do not fill a mix) |  | $ per bowl | Leave blank if you will fill the mix table below. Do not treat $7.50 as a default. That figure is a model input in the archive, not a measured average. |

## 2. Menu mix (optional path to average ticket)

Shares should add to 100%. If this block is complete, the workbook can compute the average ticket. If it is not complete, use the manual average ticket cell above.

| Bowl | Proposed price (editable assumption) | Share of bowls sold | Add-on dollars per bowl (optional) |
|---|---|---|---|
| Classic Brown Sugar and Cinnamon | 5.95 |  |  |
| Maple Walnut | 7.50 |  |  |
| Apple Pie Oats | 7.95 |  |  |
| Other / team pack / drink (describe in notes) |  |  |  |

Computed average ticket (workbook): sum of (price + add-on dollars) times share, for each row with a share.

## 3. Shared oatmeal base (cost from grocery receipts)

Use the same unit for purchase quantity and amount used (for example both in ounces, or both in grams). Cost per bowl = purchase price divided by purchase quantity, times amount used in one bowl. The three Stage 1 bowls share one plain cooked base (`pilot-and-equipment.md`).

| Ingredient | Store and brand | Purchase qty | Unit | Purchase price | Amount used per bowl | Unit | Cost per bowl | Receipt date | CHARLES FILLS THIS IN |
|---|---|---|---|---|---|---|---|---|---|
| Oats |  |  |  |  |  |  |  |  | yes, fill from receipt |
| Liquid (water, milk, or other: name it) |  |  |  |  |  |  |  |  | yes, or enter 0 for water if you use only tap water and want that stated |
| Pinch salt or other base seasoning |  |  |  |  |  |  |  |  | yes, or 0 |
| (extra row) |  |  |  |  |  |  |  |  |  |
| (extra row) |  |  |  |  |  |  |  |  |  |
| Base cost per bowl |  |  |  |  |  |  | (sum) |  | calculated in the workbook |

## 4. Toppings by bowl (cost from grocery receipts)

Add these to the shared base. Leave a row blank if that bowl does not use the item.

### Classic Brown Sugar and Cinnamon

Archive description: cinnamon, brown sugar, and (on the public menu board) butter. Raisins appear in the decision log as a possible topping. Include only what you will actually put in the bowl.

| Ingredient | Store and brand | Purchase qty | Unit | Purchase price | Amount used per bowl | Unit | Cost per bowl | Receipt date |
|---|---|---|---|---|---|---|---|---|
| Brown sugar |  |  |  |  |  |  |  |  |
| Cinnamon |  |  |  |  |  |  |  |  |
| Butter |  |  |  |  |  |  |  |  |
| Raisins (if used) |  |  |  |  |  |  |  |  |
| (extra row) |  |  |  |  |  |  |  |  |
| Classic toppings total |  |  |  |  |  |  | (sum) |  |
| Classic bowl ingredient cost |  |  |  |  |  |  | base + toppings |  |

### Maple Walnut

| Ingredient | Store and brand | Purchase qty | Unit | Purchase price | Amount used per bowl | Unit | Cost per bowl | Receipt date |
|---|---|---|---|---|---|---|---|---|
| Maple (syrup or the form you use) |  |  |  |  |  |  |  |  |
| Walnuts |  |  |  |  |  |  |  |  |
| (extra row) |  |  |  |  |  |  |  |  |
| Maple Walnut toppings total |  |  |  |  |  |  | (sum) |  |
| Maple Walnut bowl ingredient cost |  |  |  |  |  |  | base + toppings |  |

### Apple Pie Oats

Apple topping handling and storage are still subject to recipe and health review in the archive. Cost what you actually plan to use.

| Ingredient | Store and brand | Purchase qty | Unit | Purchase price | Amount used per bowl | Unit | Cost per bowl | Receipt date |
|---|---|---|---|---|---|---|---|---|
| Apples or apple topping |  |  |  |  |  |  |  |  |
| Maple or other sweetener (if used) |  |  |  |  |  |  |  |  |
| Oat crumble ingredients (list each) |  |  |  |  |  |  |  |  |
| Cinnamon or spice (if extra) |  |  |  |  |  |  |  |  |
| (extra row) |  |  |  |  |  |  |  |  |
| Apple Pie toppings total |  |  |  |  |  |  | (sum) |  |
| Apple Pie bowl ingredient cost |  |  |  |  |  |  | base + toppings |  |

Shortcut, if you are not ready to cost by recipe: enter one blended ingredient cost per bowl from a shop for a test batch, in the workbook cell labeled "Blended ingredient cost shortcut." Prefer the recipe-level table when you can.

## 5. Packaging and other per-bowl costs

| Item | Store | Purchase qty | Unit | Purchase price | Amount used per bowl | Cost per bowl | Receipt date | CHARLES FILLS THIS IN |
|---|---|---|---|---|---|---|---|---|
| Cup or bowl |  |  |  |  |  |  |  | yes |
| Lid |  |  |  |  |  |  |  | yes, or 0 if none |
| Spoon or utensil |  |  |  |  |  |  |  | yes, or 0 |
| Napkin |  |  |  |  |  |  |  | yes, or 0 |
| Sleeve, bag, or carrier |  |  |  |  |  |  |  | yes, or 0 |
| Label or sticker |  |  |  |  |  |  |  | yes, or 0 |
| (extra row) |  |  |  |  |  |  |  |  |
| Packaging total per bowl |  |  |  |  |  | (sum) |  | calculated |

| Other variable input | Value (CHARLES FILLS THIS IN) | Notes |
|---|---|---|
| Card processing fee percent |  | Enter the percent as a decimal or percent, as the workbook labels it. Leave blank if unknown; the model will treat it as $0 and list it as omitted. Do not invent a typical rate. |
| Card per-transaction fee, $ |  | Same rule as the percent. |
| Share of bowls paid by card |  | For example 1.00 if every bowl is card, 0 if all cash. Blank is treated as omitted (fee $0). |
| Spoilage and waste percent of ingredient cost |  | Blank is treated as $0 and listed as omitted. Do not invent a typical waste rate. |
| Other per-bowl cost, $ (name it in notes) |  |  |
| Host fee as a percent of ticket, if any |  | Blank is treated as $0. |

## 6. Fixed and repeating costs

Enter an amount only from a quote, a bill, or a confirmed rate. Advertised kitchen rates and published health-department example fees are in `assumptions-and-sources.md`. Do not copy them here until you confirm them.

| Cost | Amount (CHARLES FILLS THIS IN) | How often | Notes |
|---|---|---|---|
| Kitchen rental (or use the hourly block below) |  | per selling day |  |
| Kitchen hourly rate |  | $ per hour | Confirm with the kitchen. Archive advertised examples are notes only. |
| Kitchen hours reserved per selling day |  | hours | The office-channel memo's example used 2 hours. That is an example, not your booking. |
| Kitchen minimum hours, if any |  | hours | Enter 0 if there is no minimum. Blank means this line is not confirmed. |
| Fuel and vehicle cost |  | per selling day |  |
| Host site fee (flat) |  | per selling day, week, or month (say which) |  |
| Licenses and permits |  | per year or as billed | Confirm category and fee. Do not paste the archive's example CDH figures until confirmed. |
| Insurance |  | per month or year |  |
| Utilities (if you pay any beyond the kitchen rate) |  | per month |  |
| Storage |  | per month |  |
| Software or payment-device subscription (not the per-sale fee) |  | per month |  |
| Other repeating cost (name it) |  |  |  |

One-time or startup costs (kept out of weekly break-even unless you enter a recovery period):

| Cost | Amount (CHARLES FILLS THIS IN) | Notes |
|---|---|---|
| Kitchen onboarding or deposit |  |  |
| Plan review or application fees |  |  |
| Equipment and smallwares |  | Archive guidance is not to buy equipment until demand and a legal site are proven. |
| Other startup cost (name it) |  |  |
| Optional: recover startup costs over this many months |  | Leave blank to keep startup out of weekly break-even. |

## 7. Labor hours (for profit per hour, not a cash wage)

The primary break-even view does not subtract a paycheck to yourself. Hours are used only to divide profit by time. Enter 0 if a task truly takes no time.

| Activity | Hours (CHARLES FILLS THIS IN) | Period | Notes |
|---|---|---|---|
| Prep and cooking |  | per selling day |  |
| Travel, round trip |  | per selling day |  |
| Setup |  | per selling day |  |
| Service window |  | per selling day | Enter 3 if your window is the 6:30 to 9:30 a.m. hypothesis. |
| Teardown |  | per selling day |  |
| Cleaning and warewashing |  | per selling day |  |
| Shopping and receiving |  | per selling day, or say if weekly |  |
| Admin, ordering, and bookkeeping |  | per week |  |
| Other hours (name the work) |  |  |  |

Weekly hours (workbook) = (sum of per-day hours times selling days per week) + weekly-only hours.
