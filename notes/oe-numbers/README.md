# Oats, Etc. Stage 1 cost and break-even model

This folder is a blank cost template and a break-even model for the Oats, Etc. (Modern Comfort Kitchen) breakfast pilot. Stage 1 is a break-even experiment to learn from. It is not a living-wage plan, and it is not a forecast of demand.

## What the model does

You enter costs from grocery receipts and other bills, plus a ticket price and how many mornings you might sell. The model then shows the contribution on each bowl, how many bowls you need per morning and per week to cover your costs, and, if you also enter a trial volume and your hours, what is left per hour of your time. An income-target view is included as a secondary scenario only. It is not the purpose of Stage 1.

The workbook does not invent ingredient prices, rent, insurance, license fees, or how many bowls you will sell. Yellow cells are labeled CHARLES FILLS THIS IN. Until the required cells have numbers, results say "fill me in" instead of guessing. Optional costs that you leave blank are treated as $0 and are listed on the results sheet so you can see what was left out.

## Open this first

The live-formula workbook is `oats-etc-stage1-breakeven.xlsx`. It is the best way to use the model.

On a Windows PC, double-click the file to open it in Microsoft Excel. You can also upload it to Google Drive and open it with Google Sheets. There are no macros and no VBA. Edit only the yellow cells. Do not type over the calculated cells (those have a light green background).

On a phone, read this README and `markdown/cost-template.md`, or open the same Google Sheet in a mobile browser. The CSV files in `csv/` can be imported into Excel or Google Sheets if you want a starting grid without the workbook. CSV files do not contain live formulas. The workbook does.

If Excel asks how to open a CSV, choose UTF-8. The `.xlsx` file avoids that issue.

## Fill these inputs first

These are the numbers that unlock an honest break-even figure. Leave a cell blank rather than guessing.

1. Ingredient cost per bowl, from grocery receipts, for the three Stage 1 bowls: Classic Brown Sugar and Cinnamon, Maple Walnut, and Apple Pie Oats. Cost the shared plain oatmeal base once, then add toppings for each bowl.
2. Packaging cost per bowl (cup, lid, spoon, napkin, and anything else that leaves with the bowl).
3. Kitchen rental rate and hours reserved per selling day, after you confirm a kitchen. Advertised hourly rates in the research archive are notes only, not filled-in costs.
4. Average ticket, or a sales mix across the three proposed bowl prices.
5. Selling days per week. The archive has not decided whether this is 2, 3, 4, or 5 mornings.
6. Your hours per selling day (prep, travel, setup, service, teardown, cleaning) and weekly admin hours, if you want profit per hour.

Licenses, insurance, fuel, host fees, payment processing, and spoilage should be filled as soon as you have a bill or a quote. Enter 0 if that cost does not apply. Do not leave a required cell blank and assume the model will treat it as zero. Required cells are marked on the input sheets.

## Which inputs move break-even most

Break-even bowls per week equal weekly fixed costs divided by contribution per bowl. Contribution per bowl equals average ticket minus variable cost per bowl.

That contribution figure is the lever that matters most, because it sits in the denominator. When the gap between price and variable cost is thin, a small change in food cost, packaging, payment fees, or mix (for example, most people buying the $5.95 Classic with no add-on) changes the break-even count a lot. Kitchen rental is likely the largest cost that repeats every selling morning. Monthly costs such as insurance and licenses get heavier, per morning, if you sell fewer days per week. Hours worked do not change how many bowls you need to break even. They do change profit per hour once you also enter a volume.

The Sensitivity sheet shows this in both plain language and, after you fill the inputs, in a calculated table.

## What this is not

It is not a living-wage model. It is not a claim that 30 to 60 bowls will be sold. Those figures are cited hypotheses from the research archive, used only as optional scenario inputs and in a clearly labeled example. It does not choose a kitchen, a permit path, or a marketing premise. Those belong to other workstreams. It does not treat the public flavor poll as proof of paid demand.

## Files in this folder

| File | What it is |
|---|---|
| `oats-etc-stage1-breakeven.xlsx` | Workbook with live formulas. Use this in Excel or Google Sheets. |
| `assumptions-and-sources.md` | Every cited assumption, with file paths. |
| `markdown/cost-template.md` | The same input tables in Markdown, for reading on a phone or pasting into a sheet. |
| `markdown/readout-and-formulas.md` | Plain-language formulas and a short results readout. |
| `csv/` | Spreadsheet-friendly input tables without live formulas. |
| `build_workbook.py` | Script that rebuilds the `.xlsx` file. You do not need this unless you want to regenerate the workbook. Run it with Python 3 on Windows after installing openpyxl. |

## Voice of the numbers

Every pre-filled price or volume in the workbook is either a cited assumption from the repository (and labeled as such) or an EXAMPLE ONLY figure on the example sheet. If a cost is unknown, the cell is empty and marked for you to fill. Please fill from receipts and quotes, not from memory of "typical" restaurant percentages.
