#!/usr/bin/env python3
"""Build the Oats, Etc. Stage 1 break-even workbook with live Excel/Sheets formulas.

Run from this folder (Windows or this environment):
    python build_workbook.py

Requires: Python 3 and openpyxl. The workbook has no macros.
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chartsheet import Chartsheet  # noqa: F401  (keeps import map stable)
from openpyxl.worksheet.page import PageMargins

OUT_NAME = "oats-etc-stage1-breakeven.xlsx"

# Colors
NAVY = "1B4D4A"
NAVY2 = "245C58"
YELLOW = "FFF3B0"
YELLOW_DK = "6B4E00"
GREEN = "E8F5E9"
GREEN_DK = "1B5E20"
CREAM = "FFFDF8"
ORANGE = "FBE4D5"
ORANGE_DK = "C65D00"
GRAY = "F4F4F2"
GRAY_DK = "555555"
WHITE = "FFFFFF"
LINE = "C5C5C0"
RED_NOTE = "8B1E1E"
BLUE_NOTE = "1A365D"

thin = Border(
    left=Side(style="thin", color=LINE),
    right=Side(style="thin", color=LINE),
    top=Side(style="thin", color=LINE),
    bottom=Side(style="thin", color=LINE),
)
thick_bottom = Border(
    left=Side(style="thin", color=LINE),
    right=Side(style="thin", color=LINE),
    top=Side(style="thin", color=LINE),
    bottom=Side(style="medium", color=NAVY),
)

font_title = Font(name="Calibri", size=16, bold=True, color=NAVY)
font_section = Font(name="Calibri", size=12, bold=True, color=WHITE)
font_label = Font(name="Calibri", size=11, color="222222")
font_small = Font(name="Calibri", size=9, italic=True, color=GRAY_DK)
font_input = Font(name="Calibri", size=11, bold=True, color=YELLOW_DK)
font_calc = Font(name="Calibri", size=11, bold=True, color=GREEN_DK)
font_white = Font(name="Calibri", size=11, bold=True, color=WHITE)
font_warn = Font(name="Calibri", size=11, bold=True, color=ORANGE_DK)
font_header = Font(name="Calibri", size=10, bold=True, color=WHITE)
font_banner = Font(name="Calibri", size=14, bold=True, color=ORANGE_DK)
font_fillin = Font(name="Calibri", size=10, bold=True, color=RED_NOTE)

fill_navy = PatternFill("solid", fgColor=NAVY)
fill_navy2 = PatternFill("solid", fgColor=NAVY2)
fill_yellow = PatternFill("solid", fgColor=YELLOW)
fill_green = PatternFill("solid", fgColor=GREEN)
fill_cream = PatternFill("solid", fgColor=CREAM)
fill_orange = PatternFill("solid", fgColor=ORANGE)
fill_gray = PatternFill("solid", fgColor=GRAY)
fill_white = PatternFill("solid", fgColor=WHITE)

wrap = Alignment(wrap_text=True, vertical="center")
wrap_left = Alignment(wrap_text=True, vertical="center", horizontal="left")
center = Alignment(wrap_text=True, vertical="center", horizontal="center")

CUR = '"$"#,##0.00'
CUR4 = '"$"#,##0.0000'
NUM1 = "0.00"
NUM2 = "0.0"
PCT = "0.00%"
HOURS = "0.00"


def comment(text: str) -> Comment:
    c = Comment(text, "OE Numbers")
    c.width = 280
    c.height = 120
    return c


def apply_base(ws, widths: dict[str, float], tab: str, print_title: str):
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = tab
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.page_margins = PageMargins(left=0.4, right=0.4, top=0.6, bottom=0.5, header=0.25, footer=0.25)
    ws.oddHeader.left.text = print_title
    ws.oddFooter.left.text = "Oats, Etc. Stage 1  |  Break-even experiment, not a living-wage plan"
    ws.oddFooter.right.text = "Page &P of &N"
    ws.row_dimensions[1].height = 24
    for col, width in widths.items():
        ws.column_dimensions[col].width = width
    # Cream backdrop on a wide used range is heavy; keep default white and section fills instead.


def merge(ws, rng, value, font=None, fill=None, align=None, height=None):
    ws.merge_cells(rng)
    cell = ws[rng.split(":")[0]]
    cell.value = value
    cell.font = font or font_label
    if fill:
        cell.fill = fill
    cell.alignment = align or wrap_left
    if height:
        ws.row_dimensions[cell.row].height = height
    return cell


def paint(cell, *, font=None, fill=None, align=None, border=True, fmt=None, number_format=None):
    if font:
        cell.font = font
    if fill:
        cell.fill = fill
    cell.alignment = align or wrap
    if border:
        cell.border = thin
    nf = number_format or fmt
    if nf:
        cell.number_format = nf
    return cell


def header_bar(ws, row, cols, text):
    rng = f"A{row}:{cols}{row}"
    merge(ws, rng, text, font=font_section, fill=fill_navy, align=wrap, height=22)
    for col in range(1, ws[f"{cols}{row}"].column + 1):
        ws.cell(row, col).fill = fill_navy
        ws.cell(row, col).border = thin


def col_headers(ws, row, labels):
    for i, lab in enumerate(labels, 1):
        paint(ws.cell(row, i, lab), font=font_header, fill=fill_navy2, align=center)
    ws.row_dimensions[row].height = 28


def input_cell(cell, value=None, fmt=None):
    if value is not None:
        cell.value = value
    paint(cell, font=font_input, fill=fill_yellow, align=center, fmt=fmt)
    return cell


def calc_cell(cell, formula, fmt=None):
    if isinstance(formula, str) and formula and not formula.startswith("="):
        formula = "=" + formula
    cell.value = formula
    paint(cell, font=font_calc, fill=fill_green, align=center, fmt=fmt)
    return cell


def label_cell(cell, text=None):
    paint(cell, font=font_label, fill=fill_gray, align=wrap_left)
    if text is not None:
        cell.value = text
    return cell


def note_cell(cell, text=None):
    paint(cell, font=font_small, fill=fill_cream, align=wrap_left, border=True)
    if text is not None:
        cell.value = text
    return cell


def define(wb, name, sheet, cell):
    # Sheet names start with digits and must be quoted.
    ref = f"'{sheet}'!{cell}"
    existing = [n for n in wb.defined_names.keys() if n == name]
    if existing:
        del wb.defined_names[name]
    wb.defined_names.add(DefinedName(name=name, attr_text=ref))


def line_cost_formula(qty, price, amount):
    """Cost per bowl from a purchase: price / qty * amount used. Blank until all three are numbers."""
    return (
        f'IF(OR({qty}="",{price}="",{amount}=""),"",'
        f'IF(OR(NOT(ISNUMBER({qty})),NOT(ISNUMBER({price})),NOT(ISNUMBER({amount}))),"fill me in",'
        f'IF({qty}=0,"fill me in",{price}/{qty}*{amount})))'
    )


def sum_or_fill(rng, empty_message="fill me in"):
    """If no numeric costs yet, show fill-me-in (or a provided message). Otherwise sum."""
    return f'IF(COUNT({rng})=0,"{empty_message}",SUM({rng}))'


# ---------------------------------------------------------------------------
# Sheets
# ---------------------------------------------------------------------------

def build_start(wb):
    ws = wb.active
    ws.title = "00_Start_here"
    apply_base(
        ws,
        {"A": 28, "B": 28, "C": 28, "D": 28, "E": 28, "F": 22},
        NAVY,
        "Oats, Etc. Stage 1  |  Start here",
    )
    merge(
        ws,
        "A1:F1",
        "Oats, Etc. Stage 1 cost and break-even model",
        font_title,
        height=28,
    )
    merge(
        ws,
        "A2:F2",
        "A break-even experiment to learn from. This is not a living-wage plan, and it is not a sales forecast.",
        font=Font(name="Calibri", size=12, italic=True, color=NAVY),
        height=20,
    )
    merge(
        ws,
        "A3:F3",
        "Yellow cells are labeled CHARLES FILLS THIS IN. Edit only those cells. Light green cells are formulas. Do not type over them. There are no macros.",
        font=font_fillin,
        fill=fill_yellow,
        height=32,
    )

    header_bar(ws, 5, "F", "What this workbook does")
    merge(
        ws,
        "A6:F8",
        (
            "You enter costs from grocery receipts and other bills, plus a ticket price and how many mornings you might sell. "
            "The model then shows the contribution on each bowl, how many bowls you need per morning and per week to cover your costs, "
            "and, if you also enter a trial volume and your hours, what is left per hour of your time. "
            "An income-target view is included on its own tab as a secondary scenario only. It is not the purpose of Stage 1. "
            "Until required cells have numbers, results say \"fill me in\" instead of guessing."
        ),
        font=font_label,
        fill=fill_cream,
        height=36,
    )
    ws.row_dimensions[6].height = 20
    ws.row_dimensions[7].height = 20
    ws.row_dimensions[8].height = 20

    header_bar(ws, 10, "F", "How to open this on Windows or a phone")
    merge(
        ws,
        "A11:F13",
        (
            "On a Windows PC, open this file in Microsoft Excel (double-click it), or upload it to Google Drive and open it with Google Sheets. "
            "On a phone, open the same Google Sheet in a mobile browser, or read the Markdown files in the notes/oe-numbers/markdown/ folder. "
            "CSV files in notes/oe-numbers/csv/ are blank templates without live formulas. This workbook is the one with live formulas. "
            "If you rebuild the file, run build_workbook.py with Python 3 after installing openpyxl."
        ),
        font=font_label,
        fill=fill_cream,
    )
    for r in (11, 12, 13):
        ws.row_dimensions[r].height = 18

    header_bar(ws, 15, "F", "Color legend")
    paint(ws["A16"], font=font_input, fill=fill_yellow, align=center)
    ws["A16"].value = "CHARLES FILLS THIS IN"
    merge(ws, "B16:F16", "Input cells. Type numbers here, from receipts and quotes. Leave a cell blank rather than guessing. Enter 0 only when you are sure the cost does not apply.", font=font_label, fill=fill_cream)
    paint(ws["A17"], font=font_calc, fill=fill_green, align=center)
    ws["A17"].value = "Calculated"
    merge(ws, "B17:F17", "Formula cells. They show a result, or the words fill me in, until the inputs they need are filled.", font=font_label, fill=fill_cream)
    paint(ws["A18"], font=font_warn, fill=fill_orange, align=center)
    ws["A18"].value = "EXAMPLE ONLY"
    merge(ws, "B18:F18", "The Example only tab uses figures already published as illustrations in the research archive. Those numbers are not your costs and are not a forecast.", font=font_label, fill=fill_cream)
    paint(ws["A19"], font=font_small, fill=fill_gray, align=center)
    ws["A19"].value = "Notes and assumptions"
    merge(ws, "B19:F19", "Cited assumptions and source file paths. Pre-filled proposed menu prices are assumptions from the archive. They are editable.", font=font_label, fill=fill_cream)

    header_bar(ws, 21, "F", "Fill these first (required for an honest break-even)")
    firsts = [
        "1. Ingredient cost per bowl, from grocery receipts, on 02_Ingredients. Cost the shared oatmeal base once, then toppings for Classic, Maple Walnut, and Apple Pie Oats.",
        "2. Packaging per bowl (cup, lid, spoon, napkin, and anything else that leaves with the bowl) on 03_Packaging_and_fees. Enter 0 as a direct total if you truly have none.",
        "3. Kitchen rental rate and hours reserved per selling day, after you confirm a kitchen, on 04_Fixed_costs. Advertised archive rates are notes only. Enter 0 and 0 if you want to inspect a week with no kitchen charge.",
        "4. Average ticket, or a sales mix, on 01_Operations_and_menu. Proposed prices are already filled as cited assumptions. The average ticket cell is left blank on purpose.",
        "5. Selling days per week on 01_Operations_and_menu. The archive has not decided whether this is 2, 3, 4, or 5 mornings.",
        "6. Your hours, on 05_Hours, if you want profit per hour. Hours are not treated as a cash wage in the primary break-even view.",
    ]
    for i, line in enumerate(firsts):
        r = 22 + i
        merge(ws, f"A{r}:F{r}", line, font=font_label, fill=fill_cream, height=28)

    header_bar(ws, 29, "F", "Which inputs move break-even most")
    merge(
        ws,
        "A30:F32",
        (
            "Break-even bowls per week equal weekly fixed costs divided by contribution per bowl. "
            "Contribution is average ticket minus variable cost (food, packaging, and any per-bowl fees). "
            "That contribution figure is the lever that matters most, because it sits in the denominator. "
            "When the gap is thin, a small change in food cost, packaging, payment fees, or mix "
            "(for example most people buying the $5.95 Classic with no add-on) changes the break-even count a lot. "
            "Kitchen rental is likely the largest cost that repeats every selling morning. "
            "Monthly costs such as insurance and licenses get heavier, per morning, if you sell fewer days per week. "
            "Hours worked do not change how many bowls you need to break even. They do change profit per hour. "
            "See the 08_Sensitivity tab for the table that fills in after you enter costs."
        ),
        font=font_label,
        fill=fill_cream,
    )
    for r in (30, 31, 32):
        ws.row_dimensions[r].height = 22

    header_bar(ws, 34, "F", "Tabs in this workbook")
    tabs = [
        ("00_Start_here", "This page."),
        ("01_Operations_and_menu", "Days, weeks, optional volume, ticket or mix. Yellow inputs."),
        ("02_Ingredients", "Blank receipt template for the oatmeal base and three bowls."),
        ("03_Packaging_and_fees", "Cup, lid, spoon, napkin, card fees, spoilage."),
        ("04_Fixed_costs", "Kitchen, licenses, insurance, fuel, startup costs."),
        ("05_Hours", "Prep, travel, setup, service, teardown, cleaning, admin."),
        ("06_Break_even", "PRIMARY results: contribution, break-even bowls, optional profit per hour."),
        ("07_Income_target", "SECONDARY scenario only. Not the Stage 1 goal."),
        ("08_Sensitivity", "Which inputs move the answer most."),
        ("09_Example_only", "EXAMPLE ONLY kitchen-floor math from archive figures. Not your costs."),
        ("10_Sources_and_formulas", "Cited assumptions, file paths, and written-out formulas."),
    ]
    col_headers(ws, 35, ["Tab", "What it is", "", "", "", ""])
    ws.merge_cells("B35:F35")
    for i, (name, desc) in enumerate(tabs):
        r = 36 + i
        paint(ws.cell(r, 1, name), font=font_label, fill=fill_gray, align=wrap_left)
        merge(ws, f"B{r}:F{r}", desc, font=font_label, fill=fill_cream, height=18)

    header_bar(ws, 48, "F", "Honesty rules used in this model")
    merge(
        ws,
        "A49:F51",
        (
            "Every pre-filled price or volume is either a cited assumption from the repository, labeled as such, "
            "or an EXAMPLE ONLY figure on the example tab. If a cost is unknown, the cell is empty. "
            "Optional costs you leave blank (card fees, spoilage, insurance, and similar) are treated as $0 and listed on the results tab as omitted, "
            "so a partial cost picture is not mistaken for a complete one. "
            "The 30 to 60 bowls working hypothesis, the Stage 1 table of 20 to 35 bowls, and the $7.50 archive average ticket are not filled in as defaults. "
            "You may type a volume into the optional scenario cell if you want to inspect it. "
            "Sources are in 10_Sources_and_formulas and in assumptions-and-sources.md."
        ),
        font=font_label,
        fill=fill_cream,
    )
    for r in (49, 50, 51):
        ws.row_dimensions[r].height = 22

    ws.freeze_panes = "A5"
    ws.auto_filter = None
    return ws


def build_operations(wb):
    ws = wb.create_sheet("01_Operations_and_menu")
    apply_base(
        ws,
        {"A": 46, "B": 18, "C": 18, "D": 18, "E": 18, "F": 18, "G": 62},
        YELLOW.replace("FFF3B0", "E6C35C") if False else "E6C35C",
        "Oats, Etc. Stage 1  |  Operations and menu",
    )
    merge(ws, "A1:G1", "01  Operations and menu mix", font_title, height=24)
    merge(
        ws,
        "A2:G2",
        "Yellow cells: CHARLES FILLS THIS IN. Proposed bowl prices are cited assumptions from docs/oats-and-more/research/pilot-and-equipment.md and are editable. The average ticket is left blank on purpose.",
        font=font_fillin,
        fill=fill_yellow,
        height=32,
    )

    header_bar(ws, 4, "G", "Operating inputs")
    col_headers(ws, 5, ["Input", "Value", "Unit", "", "", "", "Notes"])
    rows = [
        (6, "Selling days per week", None, "days", "Required. Not decided in the archive (2, 3, 4, or 5). See docs/oats-and-more/research/decision-log.md."),
        (7, "Serving window (optional here; also enter service hours on 05_Hours)", None, "hours per selling day", "Archive hypothesis is about 6:30 to 9:30 a.m. (3 hours). Enter 3 only if that is your window."),
        (8, "Weeks per month", 4.33, "weeks", "ASSUMPTION copied from the monthly math in docs/oats-and-more/research/pilot-and-equipment.md. Edit if you prefer another convention."),
        (9, "Scenario bowls sold per selling day (optional)", None, "bowls", "Optional scenario, not a forecast. Used only to show profit at a volume you choose. Archive mentions 20 to 35 (Stage 1 table) and 30 to 60 (working hypothesis)."),
        (10, "Manual average ticket (used if the mix below is not complete)", None, "$ per bowl", "Required unless you complete the mix shares. Do not treat 7.50 as a default. That figure is a model input in the archive, not a measured average."),
    ]
    for r, label, val, unit, notes in rows:
        label_cell(ws.cell(r, 1, label))
        input_cell(ws.cell(r, 2), val, fmt=CUR if "ticket" in label.lower() else (NUM2 if r == 8 else NUM2))
        if r == 8:
            ws.cell(r, 2).number_format = "0.00"
        elif r == 10:
            ws.cell(r, 2).number_format = CUR
        elif r == 9:
            ws.cell(r, 2).number_format = NUM1
        else:
            ws.cell(r, 2).number_format = NUM1
        paint(ws.cell(r, 3, unit), font=font_small, fill=fill_cream, align=center)
        for c in (4, 5, 6):
            paint(ws.cell(r, c, ""), fill=fill_cream, border=True)
        note_cell(ws.cell(r, 7, notes))
        ws.row_dimensions[r].height = 36

    ws["B6"].comment = comment("Required. A whole number of selling mornings per week.")
    ws["B8"].comment = comment("Cited assumption: 4.33 weeks per month, from pilot-and-equipment.md. You may edit this.")
    ws["B10"].comment = comment("Leave blank if you will fill mix shares below. Do not copy 7.50 unless you mean to use that archive model input as a scenario.")

    header_bar(ws, 12, "G", "Menu mix (optional path to average ticket). Shares should add to 100.")
    col_headers(
        ws,
        13,
        [
            "Bowl",
            "Proposed price ($)",
            "Share of bowls sold (%)",
            "Add-on $ per bowl (optional)",
            "Line ticket ($)",
            "Weighted ticket ($)",
            "Notes",
        ],
    )
    bowls = [
        (14, "Classic Brown Sugar and Cinnamon", 5.95, "ASSUMPTION: working price point from docs/oats-and-more/research/pilot-and-equipment.md. Not a tested price. Share and add-ons: CHARLES FILLS THIS IN."),
        (15, "Maple Walnut", 7.50, "ASSUMPTION: working price point from the same file. Not a tested price."),
        (16, "Apple Pie Oats", 7.95, "ASSUMPTION: working price point from the same file. Apple handling and storage still subject to recipe and health review."),
        (17, "Other / team pack / drink (name it in notes)", None, "CHARLES FILLS THIS IN if you use a fourth line. Otherwise leave the row blank."),
    ]
    for r, name, price, notes in bowls:
        label_cell(ws.cell(r, 1, name))
        input_cell(ws.cell(r, 2), price, fmt=CUR)
        input_cell(ws.cell(r, 3), None, fmt=NUM1)
        input_cell(ws.cell(r, 4), None, fmt=CUR)
        # Line ticket = price + addon (addon blank counts as 0), only if price is a number
        calc_cell(
            ws.cell(r, 5),
            f'IF(NOT(ISNUMBER(B{r})),"",B{r}+IF(ISNUMBER(D{r}),D{r},0))',
            fmt=CUR,
        )
        # Weighted = line ticket * share/100 if share looks like 0-100, or * share if share is 0-1
        calc_cell(
            ws.cell(r, 6),
            (
                f'IF(OR(NOT(ISNUMBER(E{r})),NOT(ISNUMBER(C{r})),C{r}=0),"",'
                f'IF(C{r}>1,E{r}*C{r}/100,E{r}*C{r}))'
            ),
            fmt=CUR,
        )
        note_cell(ws.cell(r, 7, notes))
        ws.row_dimensions[r].height = 32

    label_cell(ws.cell(18, 1, "Mix total (shares)"))
    calc_cell(ws.cell(18, 3), "=IF(COUNT(C14:C17)=0,\"\",SUM(C14:C17))", fmt=NUM1)
    for c in (2, 4, 5):
        paint(ws.cell(18, c, ""), fill=fill_green, border=True)
    calc_cell(ws.cell(18, 6), "=IF(COUNT(F14:F17)=0,\"\",SUM(F14:F17))", fmt=CUR)
    note_cell(ws.cell(18, 7, "Shares should add to 100 (or to 1.00 if you entered decimal shares). If this block is incomplete, the manual average ticket is used instead."))
    ws.row_dimensions[18].height = 32

    header_bar(ws, 20, "G", "Ticket the rest of the workbook will use")
    label_cell(ws.cell(21, 1, "Computed average ticket from mix"))
    # Complete mix: at least one share, and the entered shares add to 100 or 1
    calc_cell(
        ws.cell(21, 2),
        (
            'IF(COUNT(C14:C17)=0,"fill me in",'
            'IF(OR(ABS(C18-100)<0.05,ABS(C18-1)<0.001),F18,"fill me in: mix shares must add to 100% or to 1"))'
        ),
        fmt=CUR,
    )
    note_cell(ws.cell(21, 7, "If shares are missing or do not add to 100 (or 1), this stays on fill me in."))
    ws.merge_cells("C21:F21")
    ws.row_dimensions[21].height = 28

    label_cell(ws.cell(22, 1, "Average ticket used by the model"))
    calc_cell(
        ws.cell(22, 2),
        'IF(ISNUMBER(B21),B21,IF(ISNUMBER(B10),B10,"fill me in"))',
        fmt=CUR,
    )
    note_cell(ws.cell(22, 7, "Prefers a complete mix when you have one. Otherwise uses the manual ticket. If both are missing, later sheets say fill me in."))
    ws.merge_cells("C22:F22")
    ws.row_dimensions[22].height = 28

    label_cell(ws.cell(23, 1, "Ticket source"))
    calc_cell(
        ws.cell(23, 2),
        'IF(ISNUMBER(B21),"mix",IF(ISNUMBER(B10),"manual ticket","fill me in"))',
    )
    note_cell(ws.cell(23, 7, "Tells you which path fed the model."))
    ws.merge_cells("C23:F23")

    define(wb, "SellingDays", ws.title, "$B$6")
    define(wb, "ServingWindow", ws.title, "$B$7")
    define(wb, "WeeksPerMonth", ws.title, "$B$8")
    define(wb, "ScenarioBowls", ws.title, "$B$9")
    define(wb, "ManualTicket", ws.title, "$B$10")
    define(wb, "TicketUsed", ws.title, "$B$22")
    define(wb, "ClassicPrice", ws.title, "$B$14")
    define(wb, "MaplePrice", ws.title, "$B$15")
    define(wb, "ApplePrice", ws.title, "$B$16")
    define(wb, "ClassicShare", ws.title, "$C$14")
    define(wb, "MapleShare", ws.title, "$C$15")
    define(wb, "AppleShare", ws.title, "$C$16")

    ws.freeze_panes = "A6"
    return ws


def write_ingredient_block(ws, start_row, title, n_rows, first_labels):
    header_bar(ws, start_row, "J", title)
    col_headers(
        ws,
        start_row + 1,
        [
            "Ingredient",
            "Store and brand",
            "Purchase qty",
            "Unit",
            "Purchase price",
            "Amount used per bowl",
            "Unit (match purchase)",
            "Cost per bowl",
            "Receipt date",
            "Notes",
        ],
    )
    first = start_row + 2
    last = first + n_rows - 1
    labels = list(first_labels) + ["(extra row)"] * (n_rows - len(first_labels))
    for i, lab in enumerate(labels):
        r = first + i
        label_cell(ws.cell(r, 1, lab))
        input_cell(ws.cell(r, 2))
        input_cell(ws.cell(r, 3), fmt=NUM1)
        input_cell(ws.cell(r, 4))
        input_cell(ws.cell(r, 5), fmt=CUR)
        input_cell(ws.cell(r, 6), fmt=NUM1)
        input_cell(ws.cell(r, 7))
        calc_cell(ws.cell(r, 8), "=" + line_cost_formula(f"C{r}", f"E{r}", f"F{r}"), fmt=CUR4)
        input_cell(ws.cell(r, 9))
        input_cell(ws.cell(r, 10))
        ws.row_dimensions[r].height = 20
    return first, last


def build_ingredients(wb):
    ws = wb.create_sheet("02_Ingredients")
    apply_base(
        ws,
        {
            "A": 36,
            "B": 22,
            "C": 14,
            "D": 12,
            "E": 15,
            "F": 18,
            "G": 16,
            "H": 15,
            "I": 14,
            "J": 42,
        },
        "E6C35C",
        "Oats, Etc. Stage 1  |  Ingredients",
    )
    merge(ws, "A1:J1", "02  Ingredient cost per bowl, from grocery receipts", font_title, height=24)
    merge(
        ws,
        "A2:J2",
        "CHARLES FILLS THIS IN. Use the same unit for purchase quantity and amount used. Cost per bowl = purchase price divided by purchase quantity, times amount used in one bowl. Do not invent prices. Leave a row blank if you do not use that item.",
        font=font_fillin,
        fill=fill_yellow,
        height=34,
    )
    merge(
        ws,
        "A3:J3",
        "The three Stage 1 bowls share one plain cooked oatmeal base (docs/oats-and-more/research/pilot-and-equipment.md). Cost the base once, then add toppings.",
        font=font_small,
        fill=fill_cream,
        height=20,
    )

    b_first, b_last = write_ingredient_block(
        ws,
        5,
        "Shared oatmeal base  |  CHARLES FILLS THIS IN from receipts",
        5,
        ["Oats", "Liquid (name water, milk, or other)", "Salt or other base seasoning"],
    )
    total_row = b_last + 1
    label_cell(ws.cell(total_row, 1, "BASE COST PER BOWL"))
    for c in range(2, 8):
        paint(ws.cell(total_row, c, ""), fill=fill_green, border=True)
    calc_cell(ws.cell(total_row, 8), f'={sum_or_fill(f"H{b_first}:H{b_last}")}', fmt=CUR4)
    note_cell(ws.cell(total_row, 10, "Sum of the base rows that have numbers. Required unless you use the blended shortcut at the bottom."))
    ws.merge_cells(f"I{total_row}:I{total_row}")
    base_total = f"$H${total_row}"
    ws.row_dimensions[total_row].height = 22

    c_first, c_last = write_ingredient_block(
        ws,
        total_row + 2,
        "Classic Brown Sugar and Cinnamon toppings  |  CHARLES FILLS THIS IN",
        5,
        ["Brown sugar", "Cinnamon", "Butter (if used)", "Raisins (if used)"],
    )
    c_sum = c_last + 1
    c_bowl = c_last + 2
    label_cell(ws.cell(c_sum, 1, "Classic toppings total"))
    for c in range(2, 8):
        paint(ws.cell(c_sum, c, ""), fill=fill_green, border=True)
    calc_cell(ws.cell(c_sum, 8), f'=IF(COUNT(H{c_first}:H{c_last})=0,0,SUM(H{c_first}:H{c_last}))', fmt=CUR4)
    note_cell(ws.cell(c_sum, 10, "If you have not entered Classic toppings yet, this shows 0 and the bowl cost stays on fill me in until the base is filled and you confirm toppings or enter 0 on a topping price with quantity 1 and amount 0."))
    label_cell(ws.cell(c_bowl, 1, "CLASSIC BOWL INGREDIENT COST (base + toppings)"))
    for c in range(2, 8):
        paint(ws.cell(c_bowl, c, ""), fill=fill_green, border=True)
    calc_cell(
        ws.cell(c_bowl, 8),
        f'IF(NOT(ISNUMBER({base_total})),"fill me in",{base_total}+IF(ISNUMBER(H{c_sum}),H{c_sum},0))',
        fmt=CUR,
    )
    note_cell(ws.cell(c_bowl, 10, "Butter is on the public menu-board description of The Classic. Raisins are mentioned in decision-log.md. Include only what you use."))
    ws.row_dimensions[c_sum].height = 28
    ws.row_dimensions[c_bowl].height = 22

    m_first, m_last = write_ingredient_block(
        ws,
        c_bowl + 2,
        "Maple Walnut toppings  |  CHARLES FILLS THIS IN",
        4,
        ["Maple (syrup or the form you use)", "Walnuts"],
    )
    m_sum = m_last + 1
    m_bowl = m_last + 2
    label_cell(ws.cell(m_sum, 1, "Maple Walnut toppings total"))
    for c in range(2, 8):
        paint(ws.cell(m_sum, c, ""), fill=fill_green, border=True)
    calc_cell(ws.cell(m_sum, 8), f'=IF(COUNT(H{m_first}:H{m_last})=0,0,SUM(H{m_first}:H{m_last}))', fmt=CUR4)
    label_cell(ws.cell(m_bowl, 1, "MAPLE WALNUT BOWL INGREDIENT COST (base + toppings)"))
    for c in range(2, 8):
        paint(ws.cell(m_bowl, c, ""), fill=fill_green, border=True)
    calc_cell(
        ws.cell(m_bowl, 8),
        f'IF(NOT(ISNUMBER({base_total})),"fill me in",{base_total}+IF(ISNUMBER(H{m_sum}),H{m_sum},0))',
        fmt=CUR,
    )
    note_cell(ws.cell(m_bowl, 10, "Walnut allergen labeling is noted as an operational issue in docs/oats-and-more/research/local-regulation.md."))
    ws.row_dimensions[m_bowl].height = 22

    a_first, a_last = write_ingredient_block(
        ws,
        m_bowl + 2,
        "Apple Pie Oats toppings  |  CHARLES FILLS THIS IN",
        5,
        ["Apples or apple topping", "Maple or other sweetener (if used)", "Oat crumble ingredient (use extra rows)", "Cinnamon or spice (if extra)"],
    )
    a_sum = a_last + 1
    a_bowl = a_last + 2
    label_cell(ws.cell(a_sum, 1, "Apple Pie toppings total"))
    for c in range(2, 8):
        paint(ws.cell(a_sum, c, ""), fill=fill_green, border=True)
    calc_cell(ws.cell(a_sum, 8), f'=IF(COUNT(H{a_first}:H{a_last})=0,0,SUM(H{a_first}:H{a_last}))', fmt=CUR4)
    label_cell(ws.cell(a_bowl, 1, "APPLE PIE BOWL INGREDIENT COST (base + toppings)"))
    for c in range(2, 8):
        paint(ws.cell(a_bowl, c, ""), fill=fill_green, border=True)
    calc_cell(
        ws.cell(a_bowl, 8),
        f'IF(NOT(ISNUMBER({base_total})),"fill me in",{base_total}+IF(ISNUMBER(H{a_sum}),H{a_sum},0))',
        fmt=CUR,
    )
    note_cell(ws.cell(a_bowl, 10, "Apple handling and storage are still subject to recipe and health review in the archive."))
    ws.row_dimensions[a_bowl].height = 22

    # Shortcut and cost used
    r = a_bowl + 2
    header_bar(ws, r, "J", "Ingredient cost the rest of the workbook will use")
    r += 1
    label_cell(ws.cell(r, 1, "Blended ingredient cost shortcut (optional)"))
    input_cell(ws.cell(r, 8), fmt=CUR)
    note_cell(ws.cell(r, 10, "CHARLES FILLS THIS IN only if you are not yet costing by recipe. Prefer the tables above when you can. Do not invent a typical food-cost percent."))
    shortcut_cell = f"$H${r}"
    ws.row_dimensions[r].height = 32
    r += 1
    label_cell(ws.cell(r, 1, "Weighted ingredient cost from mix and recipes"))
    # Weight uses shares from operations. If shares are percent (>1) divide by 100.
    # Need all three bowl costs as numbers AND a complete mix.
    calc_cell(
        ws.cell(r, 8),
        (
            f'IF(OR(NOT(ISNUMBER(H{c_bowl})),NOT(ISNUMBER(H{m_bowl})),NOT(ISNUMBER(H{a_bowl})),NOT(ISNUMBER(ClassicShare)),NOT(ISNUMBER(MapleShare)),NOT(ISNUMBER(AppleShare))),'
            f'"fill me in",'
            f'IF(ABS((ClassicShare+MapleShare+AppleShare)-100)<0.05,'
            f'(H{c_bowl}*ClassicShare+H{m_bowl}*MapleShare+H{a_bowl}*AppleShare)/100,'
            f'IF(ABS((ClassicShare+MapleShare+AppleShare)-1)<0.001,'
            f'H{c_bowl}*ClassicShare+H{m_bowl}*MapleShare+H{a_bowl}*AppleShare,'
            f'"fill me in: mix shares must add to 100% or to 1")))'
        ),
        fmt=CUR,
    )
    note_cell(ws.cell(r, 10, "Uses mix shares from 01_Operations_and_menu and the three bowl costs. Stays on fill me in until those are complete. A fourth 'Other' mix line is not included here; use the shortcut if that line matters."))
    weighted_cell = f"$H${r}"
    ws.row_dimensions[r].height = 36
    r += 1
    label_cell(ws.cell(r, 1, "Ingredient cost used by the model"))
    calc_cell(
        ws.cell(r, 8),
        f'IF(ISNUMBER({weighted_cell}),{weighted_cell},IF(ISNUMBER({shortcut_cell}),{shortcut_cell},"fill me in"))',
        fmt=CUR,
    )
    note_cell(ws.cell(r, 10, "Prefers the weighted recipe cost when the mix and recipes are complete. Otherwise uses the blended shortcut."))
    used_row = r
    ws.row_dimensions[r].height = 28

    # Flag if toppings were all left blank (base only). Informational.
    r += 2
    label_cell(ws.cell(r, 1, "Toppings status (informational)"))
    calc_cell(
        ws.cell(r, 8),
        f'IF(AND(COUNT(H{c_first}:H{c_last})=0,COUNT(H{m_first}:H{m_last})=0,COUNT(H{a_first}:H{a_last})=0),"no topping costs entered yet","topping rows have at least one cost")',
    )
    note_cell(ws.cell(r, 10, "If this says no topping costs entered yet, the bowl costs equal the base alone. That is only correct if the bowls have no topping cost."))
    ws.row_dimensions[r].height = 28

    define(wb, "BaseCost", ws.title, base_total)
    define(wb, "ClassicCost", ws.title, f"$H${c_bowl}")
    define(wb, "MapleCost", ws.title, f"$H${m_bowl}")
    define(wb, "AppleCost", ws.title, f"$H${a_bowl}")
    define(wb, "IngredientShortcut", ws.title, shortcut_cell)
    define(wb, "IngredientWeighted", ws.title, weighted_cell)
    define(wb, "IngredientUsed", ws.title, f"$H${used_row}")

    ws.freeze_panes = "A5"
    return ws


def build_packaging(wb):
    ws = wb.create_sheet("03_Packaging_and_fees")
    apply_base(
        ws,
        {
            "A": 42,
            "B": 20,
            "C": 14,
            "D": 12,
            "E": 16,
            "F": 18,
            "G": 16,
            "H": 14,
            "I": 44,
        },
        "E6C35C",
        "Oats, Etc. Stage 1  |  Packaging and fees",
    )
    merge(ws, "A1:I1", "03  Packaging and other per-bowl costs", font_title, height=24)
    merge(
        ws,
        "A2:I2",
        "CHARLES FILLS THIS IN from a receipt or supplier quote. Enter 0 only when you are sure an item is not used. Card fees and spoilage may be left blank; the workbook will then treat them as $0 and list them as omitted on the results tab.",
        font=font_fillin,
        fill=fill_yellow,
        height=34,
    )

    header_bar(ws, 4, "I", "Packaging pieces  |  CHARLES FILLS THIS IN")
    col_headers(
        ws,
        5,
        [
            "Item",
            "Store",
            "Purchase qty",
            "Unit",
            "Purchase price",
            "Amount used per bowl",
            "Cost per bowl",
            "Receipt date",
            "Notes",
        ],
    )
    items = [
        "Cup or bowl",
        "Lid",
        "Spoon or utensil",
        "Napkin",
        "Sleeve, bag, or carrier",
        "Label or sticker",
        "(extra row)",
        "(extra row)",
    ]
    first, last = 6, 5 + len(items)
    for i, name in enumerate(items):
        r = first + i
        label_cell(ws.cell(r, 1, name))
        input_cell(ws.cell(r, 2))
        input_cell(ws.cell(r, 3), fmt=NUM1)
        input_cell(ws.cell(r, 4))
        input_cell(ws.cell(r, 5), fmt=CUR)
        input_cell(ws.cell(r, 6), fmt=NUM1)
        calc_cell(ws.cell(r, 7), "=" + line_cost_formula(f"C{r}", f"E{r}", f"F{r}"), fmt=CUR4)
        input_cell(ws.cell(r, 8))
        input_cell(ws.cell(r, 9))
        ws.row_dimensions[r].height = 20
    last = first + len(items) - 1
    tot = last + 1
    label_cell(ws.cell(tot, 1, "Sum of packaging lines"))
    for c in range(2, 7):
        paint(ws.cell(tot, c, ""), fill=fill_green, border=True)
    calc_cell(ws.cell(tot, 7), f'=IF(COUNT(G{first}:G{last})=0,"fill me in",SUM(G{first}:G{last}))', fmt=CUR)
    note_cell(ws.cell(tot, 9, "Stays on fill me in until at least one packaging line has a numeric cost."))
    ws.row_dimensions[tot].height = 22

    r = tot + 1
    label_cell(ws.cell(r, 1, "Direct packaging total (optional override or enter 0 if none)"))
    input_cell(ws.cell(r, 7), fmt=CUR)
    note_cell(ws.cell(r, 9, "CHARLES FILLS THIS IN if you want a single packaging number, or enter 0 if you truly have no packaging. Used when the line sum is still fill me in."))
    direct = f"$G${r}"
    ws.row_dimensions[r].height = 32
    r += 1
    label_cell(ws.cell(r, 1, "Packaging cost used by the model"))
    calc_cell(
        ws.cell(r, 7),
        f'IF(ISNUMBER(G{tot}),G{tot},IF(ISNUMBER({direct}),{direct},"fill me in"))',
        fmt=CUR,
    )
    note_cell(ws.cell(r, 9, "Prefers the line-item sum. Otherwise uses the direct total, including a confirmed 0."))
    pack_used = f"$G${r}"
    pack_used_row = r

    r += 2
    header_bar(ws, r, "I", "Other variable amounts  |  blank is treated as $0 and listed as omitted")
    r += 1
    col_headers(ws, r, ["Input", "Value", "Unit", "", "", "", "Calculated $ per bowl", "", "Notes"])
    r += 1
    other_start = r
    fields = [
        ("Card processing fee percent", "percent; enter 2.9 for 2.9%", "Leave blank if unknown. Do not invent a typical processor rate."),
        ("Card per-transaction fee", "$ per paid card bowl", "Leave blank if unknown."),
        ("Share of bowls paid by card", "1.00 = all card; 0 = all cash. You may also enter 80 for 80%.", "Blank means the fee is omitted."),
        ("Spoilage and waste percent of ingredient cost", "percent; enter 5 for 5%", "Leave blank if unknown. Do not invent a typical waste rate."),
        ("Other per-bowl cost", "$", "Name the cost in the notes column."),
        ("Host fee as a percent of ticket", "percent; enter 10 for 10%", "Blank is treated as $0 and listed as omitted."),
    ]
    # rows: r, r+1, ...
    for i, (lab, unit, notes) in enumerate(fields):
        rr = r + i
        label_cell(ws.cell(rr, 1, lab))
        input_cell(ws.cell(rr, 2), fmt=NUM1)
        paint(ws.cell(rr, 3, unit), font=font_small, fill=fill_cream, align=center)
        for c in (4, 5, 6, 8):
            paint(ws.cell(rr, c, ""), fill=fill_cream, border=True)
        note_cell(ws.cell(rr, 9, notes))
        ws.row_dimensions[rr].height = 30
    card_pct, card_fee, card_share, spoil, other, host = range(r, r + 6)

    # Calculated fee components
    # Normalize percent: if value > 1, treat as 2.9 meaning 2.9%, else as already decimal (0.029)
    def pct_as_frac(cell):
        return f"IF({cell}>1,{cell}/100,{cell})"

    def share_as_frac(cell):
        return f"IF({cell}>1,{cell}/100,{cell})"

    calc_cell(
        ws.cell(card_pct, 7),
        (
            f'IF(OR(NOT(ISNUMBER(B{card_pct})),NOT(ISNUMBER(B{card_fee})),NOT(ISNUMBER(B{card_share})),NOT(ISNUMBER(TicketUsed))),'
            f'"",'
            f'(TicketUsed*{pct_as_frac(f"B{card_pct}")}+B{card_fee})*{share_as_frac(f"B{card_share}")})'
        ),
        fmt=CUR4,
    )
    # leave G for card_fee and card_share empty (the fee is one combined number on the first of the three)
    paint(ws.cell(card_fee, 7, ""), fill=fill_green, border=True)
    paint(ws.cell(card_share, 7, ""), fill=fill_green, border=True)
    calc_cell(
        ws.cell(spoil, 7),
        (
            f'IF(OR(NOT(ISNUMBER(B{spoil})),NOT(ISNUMBER(IngredientUsed))),"",'
            f'IngredientUsed*{pct_as_frac(f"B{spoil}")})'
        ),
        fmt=CUR4,
    )
    calc_cell(
        ws.cell(other, 7),
        f'IF(NOT(ISNUMBER(B{other})),"",B{other})',
        fmt=CUR4,
    )
    calc_cell(
        ws.cell(host, 7),
        (
            f'IF(OR(NOT(ISNUMBER(B{host})),NOT(ISNUMBER(TicketUsed))),"",'
            f'TicketUsed*{pct_as_frac(f"B{host}")})'
        ),
        fmt=CUR4,
    )

    r = host + 2
    header_bar(ws, r, "I", "Variable cost per bowl used by the model")
    r += 1
    label_cell(ws.cell(r, 1, "Payment fee per bowl (0 if card fields are incomplete)"))
    calc_cell(ws.cell(r, 7), f'IF(ISNUMBER(G{card_pct}),G{card_pct},0)', fmt=CUR4)
    pay_row = r
    r += 1
    label_cell(ws.cell(r, 1, "Spoilage per bowl (0 if spoilage percent is blank)"))
    calc_cell(ws.cell(r, 7), f'IF(ISNUMBER(G{spoil}),G{spoil},0)', fmt=CUR4)
    spoil_row = r
    r += 1
    label_cell(ws.cell(r, 1, "Other per-bowl cost (0 if blank)"))
    calc_cell(ws.cell(r, 7), f'IF(ISNUMBER(G{other}),G{other},0)', fmt=CUR4)
    other_row = r
    r += 1
    label_cell(ws.cell(r, 1, "Host percent fee per bowl (0 if blank)"))
    calc_cell(ws.cell(r, 7), f'IF(ISNUMBER(G{host}),G{host},0)', fmt=CUR4)
    host_row = r
    r += 1
    label_cell(ws.cell(r, 1, "Variable cost per bowl (V)"))
    calc_cell(
        ws.cell(r, 7),
        (
            f'IF(OR(NOT(ISNUMBER(IngredientUsed)),NOT(ISNUMBER({pack_used}))),"fill me in",'
            f'IngredientUsed+{pack_used}+G{pay_row}+G{spoil_row}+G{other_row}+G{host_row})'
        ),
        fmt=CUR,
    )
    note_cell(ws.cell(r, 9, "Requires ingredient cost and packaging cost. Adds any of the optional fees that have numbers."))
    var_row = r
    ws.row_dimensions[r].height = 28
    r += 1
    label_cell(ws.cell(r, 1, "Omitted optional variable lines"))
    calc_cell(
        ws.cell(r, 7),
        (
            f'TRIM(CONCATENATE('
            f'IF(ISNUMBER(B{card_pct})+ISNUMBER(B{card_fee})+ISNUMBER(B{card_share})=3,"",'
            f'IF(COUNT(B{card_pct},B{card_fee},B{card_share})=0,"card fees; ","card fees (incomplete, treated as $0); ")),'
            f'IF(ISNUMBER(B{spoil}),"","spoilage; "),'
            f'IF(ISNUMBER(B{other}),"","other per-bowl cost; "),'
            f'IF(ISNUMBER(B{host}),"","host percent fee; ")))'
        ),
    )
    note_cell(ws.cell(r, 9, "These optional items were left blank and are treated as $0. A trailing semicolon is harmless."))
    omit_row = r
    ws.merge_cells(f"G{r}:H{r}")
    ws.row_dimensions[r].height = 32

    define(wb, "PackagingUsed", ws.title, pack_used)
    define(wb, "PaymentFee", ws.title, f"$G${pay_row}")
    define(wb, "SpoilageCost", ws.title, f"$G${spoil_row}")
    define(wb, "OtherVariable", ws.title, f"$G${other_row}")
    define(wb, "HostFeePerBowl", ws.title, f"$G${host_row}")
    define(wb, "VariableUsed", ws.title, f"$G${var_row}")
    define(wb, "OmittedVariable", ws.title, f"$G${omit_row}")
    define(wb, "CardPct", ws.title, f"$B${card_pct}")
    define(wb, "CardFee", ws.title, f"$B${card_fee}")
    define(wb, "CardShare", ws.title, f"$B${card_share}")
    define(wb, "SpoilPct", ws.title, f"$B${spoil}")
    define(wb, "HostPct", ws.title, f"$B${host}")

    ws.freeze_panes = "A5"
    return ws




def weekly_amount_formula(amount_cell, freq_cell):
    return (
        f'IF(OR({amount_cell}="",NOT(ISNUMBER({amount_cell}))),0,'
        f'IF({freq_cell}="",' "\"fill me in\","
        f'IF({freq_cell}="per selling day",'
        f'IF(NOT(ISNUMBER(SellingDays)),"fill me in",{amount_cell}*SellingDays),'
        f'IF({freq_cell}="per week",{amount_cell},'
        f'IF({freq_cell}="per month",'
        f'IF(NOT(ISNUMBER(WeeksPerMonth)),"fill me in",{amount_cell}/WeeksPerMonth),'
        f'IF({freq_cell}="per year",{amount_cell}/52,'
        f'"fill me in: choose frequency"))))))'
    )


def build_fixed(wb):
    ws = wb.create_sheet("04_Fixed_costs")
    apply_base(
        ws,
        {"A": 50, "B": 16, "C": 22, "D": 16, "E": 16, "F": 18, "G": 52},
        "E6C35C",
        "Oats, Etc. Stage 1  |  Fixed costs",
    )
    merge(ws, "A1:G1", "04  Fixed, repeating, and startup costs", font_title, height=24)
    merge(
        ws,
        "A2:G2",
        "CHARLES FILLS THIS IN from a confirmed quote or bill. Advertised kitchen rates and example health-department fees in the research archive are notes only. Do not copy them here until confirmed. See 10_Sources_and_formulas.",
        font=font_fillin,
        fill=fill_yellow,
        height=34,
    )
    merge(
        ws,
        "A3:G3",
        "If you want to inspect break-even with no kitchen charge, enter 0 for the hourly rate and 0 for hours reserved. Leaving them blank keeps results on fill me in, because kitchen rent is expected to be a major daily cost.",
        font=font_small,
        fill=fill_cream,
        height=28,
    )

    header_bar(ws, 5, "G", "Kitchen rental  |  CHARLES FILLS THIS IN after you confirm a kitchen")
    col_headers(ws, 6, ["Input", "Value", "Unit", "", "", "Calculated", "Notes"])

    kitchen_rows = [
        (7, "Kitchen hourly rate", CUR, "$ per hour", "Confirm with the kitchen. Archive advertised examples (Gina's $40, Flava $30, Commons $40/$20, Osage $35/$25) are not filled in here. See docs/oats-and-more/research/boise-kitchen-and-office-service-market-2026-11-11.md."),
        (8, "Kitchen hours reserved per selling day", NUM1, "hours", "The office-channel memo's illustrative check used 2 hours. That is an example, not your booking."),
        (9, "Kitchen minimum hours, if any", NUM1, "hours", "Enter 0 if there is no minimum. If you leave this blank, the workbook uses reserved hours only, once a rate and reserved hours exist."),
    ]
    for r, lab, fmt, unit, notes in kitchen_rows:
        label_cell(ws.cell(r, 1, lab))
        input_cell(ws.cell(r, 2), fmt=fmt)
        paint(ws.cell(r, 3, unit), font=font_small, fill=fill_cream, align=center)
        for c in (4, 5):
            paint(ws.cell(r, c, ""), fill=fill_cream, border=True)
        paint(ws.cell(r, 6, ""), fill=fill_green, border=True)
        note_cell(ws.cell(r, 7, notes))
        ws.row_dimensions[r].height = 36

    label_cell(ws.cell(10, 1, "Kitchen cost per selling day"))
    for c in (2, 3, 4, 5):
        paint(ws.cell(10, c, ""), fill=fill_green, border=True)
    calc_cell(
        ws.cell(10, 6),
        'IF(OR(NOT(ISNUMBER(B7)),NOT(ISNUMBER(B8))),"fill me in",B7*MAX(B8,IF(ISNUMBER(B9),B9,0)))',
        fmt=CUR,
    )
    note_cell(ws.cell(10, 7, "Rate times the larger of reserved hours and a numeric minimum. Enter 0 and 0 to model no kitchen charge."))
    ws.row_dimensions[10].height = 28

    label_cell(ws.cell(11, 1, "Kitchen cost per week"))
    for c in (2, 3, 4, 5):
        paint(ws.cell(11, c, ""), fill=fill_green, border=True)
    calc_cell(
        ws.cell(11, 6),
        'IF(OR(NOT(ISNUMBER(F10)),NOT(ISNUMBER(SellingDays))),"fill me in",F10*SellingDays)',
        fmt=CUR,
    )
    note_cell(ws.cell(11, 7, "Per-day kitchen cost times selling days per week."))
    ws.row_dimensions[11].height = 24

    header_bar(ws, 13, "G", "Other repeating costs  |  blank amounts are treated as $0 and listed as omitted")
    col_headers(ws, 14, ["Cost", "Amount", "How often", "", "", "Weekly amount", "Notes"])

    other = [
        (15, "Fuel and vehicle", "per selling day", "Blank amount is treated as $0 and listed as omitted."),
        (16, "Host site fee (flat)", "per selling day", "Change the frequency if this is weekly or monthly. Blank amount is $0."),
        (17, "Licenses and permits", "per year", "Do not paste the archive's example Central District Health figures until you confirm category and fee. See local-regulation.md."),
        (18, "Insurance", "per month", "Blank amount is $0 and listed as omitted."),
        (19, "Utilities (beyond the kitchen rate)", "per month", "Blank amount is $0."),
        (20, "Storage", "per month", "Blank amount is $0."),
        (21, "Software or payment-device subscription (not the per-sale fee)", "per month", "Blank amount is $0."),
        (22, "Other repeating cost (name it in notes)", "", "Choose a frequency if you enter an amount."),
        (23, "Other repeating cost (name it in notes)", "", ""),
    ]
    dv = DataValidation(
        type="list",
        formula1='"per selling day,per week,per month,per year"',
        allow_blank=True,
    )
    dv.error = "Choose per selling day, per week, per month, or per year."
    dv.errorTitle = "Frequency"
    dv.prompt = "Choose how often this cost is billed."
    dv.promptTitle = "Frequency"
    ws.add_data_validation(dv)
    dv.add("C15:C23")

    for r, name, freq, notes in other:
        label_cell(ws.cell(r, 1, name))
        input_cell(ws.cell(r, 2), fmt=CUR)
        input_cell(ws.cell(r, 3), freq)
        # Frequency is a yellow input; pre-filled frequencies are suggestions, not facts.
        if freq:
            ws.cell(r, 3).comment = comment(
                "Suggested frequency, not a confirmed bill. Change it if your bill is on a different cycle. This is not a measured cost."
            )
        for c in (4, 5):
            paint(ws.cell(r, c, ""), fill=fill_cream, border=True)
        calc_cell(ws.cell(r, 6), "=" + weekly_amount_formula(f"B{r}", f"C{r}"), fmt=CUR)
        note_cell(ws.cell(r, 7, notes))
        ws.row_dimensions[r].height = 28

    label_cell(ws.cell(24, 1, "Other repeating costs per week"))
    for c in (2, 3, 4, 5):
        paint(ws.cell(24, c, ""), fill=fill_green, border=True)
    calc_cell(
        ws.cell(24, 6),
        'IF(COUNTIF(F15:F23,"fill me in*")>0,"fill me in",SUM(F15:F23))',
        fmt=CUR,
    )
    note_cell(ws.cell(24, 7, "If any row has an amount but no frequency, this stays on fill me in."))
    ws.row_dimensions[24].height = 24

    header_bar(ws, 26, "G", "Startup and one-time costs  |  kept out of weekly break-even unless you enter a recovery period")
    col_headers(ws, 27, ["Cost", "Amount", "", "", "", "", "Notes"])
    startups = [
        (28, "Kitchen onboarding or deposit", "Kept out of weekly break-even unless you enter a recovery period below."),
        (29, "Plan review or application fees", "Published example fees in local-regulation.md must be confirmed before use."),
        (30, "Equipment and smallwares", "Archive guidance is not to buy equipment until demand and a legal site are proven (research/README.md)."),
        (31, "Other startup cost (name it in notes)", ""),
        (32, "Other startup cost (name it in notes)", ""),
    ]
    for r, name, notes in startups:
        label_cell(ws.cell(r, 1, name))
        input_cell(ws.cell(r, 2), fmt=CUR)
        for c in (3, 4, 5, 6):
            paint(ws.cell(r, c, ""), fill=fill_cream, border=True)
        note_cell(ws.cell(r, 7, notes))
        ws.row_dimensions[r].height = 24

    label_cell(ws.cell(33, 1, "Startup total"))
    calc_cell(ws.cell(33, 2), '=IF(COUNT(B28:B32)=0,0,SUM(B28:B32))', fmt=CUR)
    for c in (3, 4, 5, 6):
        paint(ws.cell(33, c, ""), fill=fill_green, border=True)
    note_cell(ws.cell(33, 7, "Sum of the one-time amounts you entered. 0 if all are blank."))

    label_cell(ws.cell(34, 1, "Optional: recover startup over this many months"))
    input_cell(ws.cell(34, 2), fmt=NUM1)
    note_cell(ws.cell(34, 7, "CHARLES FILLS THIS IN only if you want startup rolled into weekly break-even. Leave blank to keep startup out."))
    ws.row_dimensions[34].height = 28

    label_cell(ws.cell(35, 1, "Startup amount included per week (0 if no recovery period)"))
    calc_cell(
        ws.cell(35, 6),
        'IF(OR(NOT(ISNUMBER(B34)),B34<=0,NOT(ISNUMBER(B33)),NOT(ISNUMBER(WeeksPerMonth))),0,B33/B34/WeeksPerMonth)',
        fmt=CUR,
    )
    for c in (2, 3, 4, 5):
        paint(ws.cell(35, c, ""), fill=fill_green, border=True)
    note_cell(ws.cell(35, 7, "Startup total divided by recovery months, then divided by weeks per month."))

    header_bar(ws, 37, "G", "Weekly fixed cost used by the model")
    label_cell(ws.cell(38, 1, "Weekly fixed cost (F)"))
    calc_cell(
        ws.cell(38, 6),
        'IF(OR(NOT(ISNUMBER(F11)),NOT(ISNUMBER(F24)),NOT(ISNUMBER(F35))),"fill me in",F11+F24+F35)',
        fmt=CUR,
    )
    for c in (2, 3, 4, 5):
        paint(ws.cell(38, c, ""), fill=fill_green, border=True)
    note_cell(ws.cell(38, 7, "Kitchen per week, plus other repeating costs per week, plus any startup recovery."))
    ws.row_dimensions[38].height = 26

    label_cell(ws.cell(39, 1, "Omitted optional fixed lines"))
    calc_cell(
        ws.cell(39, 6),
        (
            'TRIM(CONCATENATE('
            'IF(ISNUMBER(B15),"","fuel; "),'
            'IF(ISNUMBER(B16),"","host fee; "),'
            'IF(ISNUMBER(B17),"","licenses; "),'
            'IF(ISNUMBER(B18),"","insurance; "),'
            'IF(ISNUMBER(B19),"","utilities; "),'
            'IF(ISNUMBER(B20),"","storage; "),'
            'IF(ISNUMBER(B21),"","software; "),'
            'IF(ISNUMBER(B22),"","other repeating (row 22); "),'
            'IF(ISNUMBER(B23),"","other repeating (row 23); ")))'
        ),
    )
    ws.merge_cells("F39:F39")
    note_cell(ws.cell(39, 7, "These optional items were left blank and are treated as $0."))
    ws.row_dimensions[39].height = 32

    define(wb, "KitchenRate", ws.title, "$B$7")
    define(wb, "KitchenHours", ws.title, "$B$8")
    define(wb, "KitchenMinHours", ws.title, "$B$9")
    define(wb, "KitchenPerDay", ws.title, "$F$10")
    define(wb, "KitchenPerWeek", ws.title, "$F$11")
    define(wb, "OtherFixedWeek", ws.title, "$F$24")
    define(wb, "StartupTotal", ws.title, "$B$33")
    define(wb, "StartupMonths", ws.title, "$B$34")
    define(wb, "StartupPerWeek", ws.title, "$F$35")
    define(wb, "FixedWeekly", ws.title, "$F$38")
    define(wb, "OmittedFixed", ws.title, "$F$39")

    ws.freeze_panes = "A6"
    return ws


def build_hours(wb):
    ws = wb.create_sheet("05_Hours")
    apply_base(
        ws,
        {"A": 46, "B": 14, "C": 22, "D": 16, "E": 16, "F": 18, "G": 56},
        "E6C35C",
        "Oats, Etc. Stage 1  |  Hours",
    )
    merge(ws, "A1:G1", "05  Labor hours (for profit per hour, not a cash wage)", font_title, height=24)
    merge(
        ws,
        "A2:G2",
        "CHARLES FILLS THIS IN. The primary break-even view does not subtract a paycheck to yourself. Hours are used only to divide profit by time. Stage 1 is not a living-wage model. Enter 0 if a task truly takes no time. If this whole sheet is left blank, profit per hour stays on fill me in, and break-even bowls can still compute.",
        font=font_fillin,
        fill=fill_yellow,
        height=40,
    )

    header_bar(ws, 4, "G", "Hours per selling day")
    col_headers(ws, 5, ["Activity", "Hours", "Period", "", "", "", "Notes"])
    day_rows = [
        (6, "Prep and cooking", "per selling day", ""),
        (7, "Travel, round trip", "per selling day", ""),
        (8, "Setup", "per selling day", ""),
        (9, "Service window", "per selling day", "Enter 3 if your window is the 6:30 to 9:30 a.m. hypothesis in docs/oats-and-more/research/decision-log.md."),
        (10, "Teardown", "per selling day", ""),
        (11, "Cleaning and warewashing", "per selling day", ""),
        (12, "Shopping and receiving", "per selling day", "If this is weekly instead, put it in the weekly admin row and say so in the notes."),
        (13, "Other hours per selling day (name the work in notes)", "per selling day", ""),
    ]
    for r, lab, period, notes in day_rows:
        label_cell(ws.cell(r, 1, lab))
        input_cell(ws.cell(r, 2), fmt=HOURS)
        paint(ws.cell(r, 3, period), font=font_small, fill=fill_cream, align=center)
        for c in (4, 5, 6):
            paint(ws.cell(r, c, ""), fill=fill_cream, border=True)
        note_cell(ws.cell(r, 7, notes))
        ws.row_dimensions[r].height = 24

    label_cell(ws.cell(14, 1, "Hours per selling day"))
    calc_cell(
        ws.cell(14, 2),
        'IF(COUNT(B6:B13)=0,"fill me in",SUM(B6:B13))',
        fmt=HOURS,
    )
    note_cell(ws.cell(14, 7, "Sum of the per-day rows that have numbers. Blank rows count as 0 only after at least one row is filled."))
    ws.row_dimensions[14].height = 28
    for c in (3, 4, 5, 6):
        paint(ws.cell(14, c, ""), fill=fill_green, border=True)

    header_bar(ws, 16, "G", "Weekly-only hours")
    label_cell(ws.cell(17, 1, "Admin, ordering, and bookkeeping"))
    input_cell(ws.cell(17, 2), fmt=HOURS)
    paint(ws.cell(17, 3, "per week"), font=font_small, fill=fill_cream, align=center)
    note_cell(ws.cell(17, 7, "CHARLES FILLS THIS IN. Enter 0 if none."))
    label_cell(ws.cell(18, 1, "Other weekly hours (name the work in notes)"))
    input_cell(ws.cell(18, 2), fmt=HOURS)
    paint(ws.cell(18, 3, "per week"), font=font_small, fill=fill_cream, align=center)
    note_cell(ws.cell(18, 7, ""))

    header_bar(ws, 20, "G", "Weekly hours used by the model")
    label_cell(ws.cell(21, 1, "Weekly hours"))
    calc_cell(
        ws.cell(21, 2),
        (
            'IF(OR(NOT(ISNUMBER(B14)),NOT(ISNUMBER(SellingDays))),"fill me in",'
            'B14*SellingDays+IF(ISNUMBER(B17),B17,0)+IF(ISNUMBER(B18),B18,0))'
        ),
        fmt=HOURS,
    )
    note_cell(ws.cell(21, 7, "(Hours per selling day times selling days per week) plus weekly-only hours. Stays on fill me in until per-day hours and selling days are numbers."))
    for c in (3, 4, 5, 6):
        paint(ws.cell(21, c, ""), fill=fill_green, border=True)
    ws.row_dimensions[21].height = 32

    define(wb, "HoursPerDay", ws.title, "$B$14")
    define(wb, "HoursWeekly", ws.title, "$B$21")
    ws.freeze_panes = "A6"
    return ws


def build_breakeven(wb):
    ws = wb.create_sheet("06_Break_even")
    apply_base(
        ws,
        {"A": 52, "B": 22, "C": 18, "D": 18, "E": 18, "F": 62},
        "3D8B6E",
        "Oats, Etc. Stage 1  |  Break-even (primary)",
    )
    merge(ws, "A1:F1", "06  Break-even results  |  PRIMARY VIEW", font_title, height=24)
    merge(
        ws,
        "A2:F2",
        "This tab answers the Stage 1 question: how many bowls cover the cash costs you entered, and, if you also entered a volume and hours, what is left per hour of your time. This is not a living-wage plan and not a forecast.",
        font=Font(name="Calibri", size=11, italic=True, color=NAVY),
        fill=fill_cream,
        height=32,
    )

    header_bar(ws, 4, "F", "Input checklist  (green formulas; they stay on fill me in until the source cells are numbers)")
    col_headers(ws, 5, ["Item", "Status", "", "", "", "Notes"])
    checks = [
        (6, "Average ticket (T)", "=IF(ISNUMBER(TicketUsed),TicketUsed,\"fill me in\")", CUR, "From 01_Operations_and_menu."),
        (7, "Ingredient cost per bowl", "=IF(ISNUMBER(IngredientUsed),IngredientUsed,\"fill me in\")", CUR, "From 02_Ingredients."),
        (8, "Packaging cost per bowl", "=IF(ISNUMBER(PackagingUsed),PackagingUsed,\"fill me in\")", CUR, "From 03_Packaging_and_fees."),
        (9, "Selling days per week", "=IF(ISNUMBER(SellingDays),SellingDays,\"fill me in\")", NUM1, "From 01_Operations_and_menu."),
        (10, "Kitchen cost per selling day", "=IF(ISNUMBER(KitchenPerDay),KitchenPerDay,\"fill me in\")", CUR, "From 04_Fixed_costs. Enter 0 and 0 there to model no kitchen charge."),
        (11, "Weekly fixed cost (F)", "=IF(ISNUMBER(FixedWeekly),FixedWeekly,\"fill me in\")", CUR, "Kitchen plus other repeating costs plus any startup recovery."),
    ]
    for r, lab, formula, fmt, notes in checks:
        label_cell(ws.cell(r, 1, lab))
        calc_cell(ws.cell(r, 2), formula, fmt=fmt)
        for c in (3, 4, 5):
            paint(ws.cell(r, c, ""), fill=fill_green, border=True)
        note_cell(ws.cell(r, 6, notes))
        ws.row_dimensions[r].height = 22

    header_bar(ws, 13, "F", "Contribution per bowl")
    lines = [
        (14, "Average ticket (T)", "=IF(ISNUMBER(TicketUsed),TicketUsed,\"fill me in\")", CUR, "The ticket the model is using."),
        (15, "Ingredient cost", "=IF(ISNUMBER(IngredientUsed),IngredientUsed,\"fill me in\")", CUR, ""),
        (16, "Packaging", "=IF(ISNUMBER(PackagingUsed),PackagingUsed,\"fill me in\")", CUR, ""),
        (17, "Payment fee", "=IF(ISNUMBER(PaymentFee),PaymentFee,0)", CUR, "0 if card fields were left blank."),
        (18, "Spoilage", "=IF(ISNUMBER(SpoilageCost),SpoilageCost,0)", CUR, "0 if spoilage was left blank."),
        (19, "Other per-bowl cost", "=IF(ISNUMBER(OtherVariable),OtherVariable,0)", CUR, ""),
        (20, "Host percent fee", "=IF(ISNUMBER(HostFeePerBowl),HostFeePerBowl,0)", CUR, ""),
        (21, "Variable cost per bowl (V)", "=IF(ISNUMBER(VariableUsed),VariableUsed,\"fill me in\")", CUR, "Ingredients + packaging + the optional fees that have numbers."),
        (22, "Contribution per bowl (C = T minus V)", 
         '=IF(OR(NOT(ISNUMBER(TicketUsed)),NOT(ISNUMBER(VariableUsed))),"fill me in",TicketUsed-VariableUsed)',
         CUR, "If this is zero or negative, there is no break-even at this ticket."),
    ]
    # I already called header_bar on 13 then col_headers would overwrite. Let me fix: header is 13, headers should be 14, data starts 15.
    # Oops I already set data at 14. Let me not use col_headers on 13 after header_bar. The header_bar already filled row 13. I'll put labels in column A and values in B, notes in F. Skip a second header. Good as written if I don't call col_headers. I did call header_bar only. Good.

    for r, lab, formula, fmt, notes in lines:
        label_cell(ws.cell(r, 1, lab))
        calc_cell(ws.cell(r, 2), formula, fmt=fmt)
        for c in (3, 4, 5):
            paint(ws.cell(r, c, ""), fill=fill_green, border=True)
        note_cell(ws.cell(r, 6, notes))
        ws.row_dimensions[r].height = 22
    ws.row_dimensions[22].height = 26

    header_bar(ws, 24, "F", "Break-even bowls  (primary result)")
    label_cell(ws.cell(25, 1, "Break-even bowls per week"))
    calc_cell(
        ws.cell(25, 2),
        (
            'IF(OR(NOT(ISNUMBER(FixedWeekly)),NOT(ISNUMBER(B22))),"fill me in",'
            'IF(B22<=0,"ticket must be higher than variable cost",FixedWeekly/B22))'
        ),
        fmt=NUM1,
    )
    note_cell(ws.cell(25, 6, "Weekly fixed cost divided by contribution per bowl."))
    ws.row_dimensions[25].height = 26

    label_cell(ws.cell(26, 1, "Break-even bowls per selling day"))
    calc_cell(
        ws.cell(26, 2),
        'IF(OR(NOT(ISNUMBER(B25)),NOT(ISNUMBER(SellingDays)),SellingDays=0),"fill me in",B25/SellingDays)',
        fmt=NUM1,
    )
    note_cell(ws.cell(26, 6, "Weekly break-even divided by selling days per week."))

    label_cell(ws.cell(27, 1, "Break-even bowls per month"))
    calc_cell(
        ws.cell(27, 2),
        'IF(OR(NOT(ISNUMBER(B25)),NOT(ISNUMBER(WeeksPerMonth))),"fill me in",B25*WeeksPerMonth)',
        fmt=NUM1,
    )
    note_cell(ws.cell(27, 6, "Weekly break-even times weeks per month (default assumption 4.33)."))

    header_bar(ws, 29, "F", "If you entered an optional scenario volume")
    label_cell(ws.cell(30, 1, "Scenario bowls per selling day"))
    calc_cell(ws.cell(30, 2), '=IF(ISNUMBER(ScenarioBowls),ScenarioBowls,"fill me in")', fmt=NUM1)
    note_cell(ws.cell(30, 6, "Optional. This is a scenario you typed, not a forecast."))

    label_cell(ws.cell(31, 1, "Scenario bowls per week"))
    calc_cell(
        ws.cell(31, 2),
        'IF(OR(NOT(ISNUMBER(ScenarioBowls)),NOT(ISNUMBER(SellingDays))),"fill me in",ScenarioBowls*SellingDays)',
        fmt=NUM1,
    )
    note_cell(ws.cell(31, 6, "Scenario bowls per day times selling days."))

    label_cell(ws.cell(32, 1, "Weekly gross sales at that volume"))
    calc_cell(
        ws.cell(32, 2),
        'IF(OR(NOT(ISNUMBER(TicketUsed)),NOT(ISNUMBER(B31))),"fill me in",TicketUsed*B31)',
        fmt=CUR,
    )
    note_cell(ws.cell(32, 6, "Average ticket times scenario bowls per week. This is gross, not profit."))

    label_cell(ws.cell(33, 1, "Weekly contribution at that volume"))
    calc_cell(
        ws.cell(33, 2),
        'IF(OR(NOT(ISNUMBER(B22)),NOT(ISNUMBER(B31))),"fill me in",B22*B31)',
        fmt=CUR,
    )
    note_cell(ws.cell(33, 6, "Contribution per bowl times scenario bowls per week."))

    label_cell(ws.cell(34, 1, "Weekly profit at that volume (no operator wage)"))
    calc_cell(
        ws.cell(34, 2),
        'IF(OR(NOT(ISNUMBER(B33)),NOT(ISNUMBER(FixedWeekly))),"fill me in",B33-FixedWeekly)',
        fmt=CUR,
    )
    note_cell(ws.cell(34, 6, "Weekly contribution minus weekly fixed cost. Operator time is not a cash wage here."))
    ws.row_dimensions[34].height = 26

    label_cell(ws.cell(35, 1, "Monthly profit at that volume"))
    calc_cell(
        ws.cell(35, 2),
        'IF(OR(NOT(ISNUMBER(B34)),NOT(ISNUMBER(WeeksPerMonth))),"fill me in",B34*WeeksPerMonth)',
        fmt=CUR,
    )
    note_cell(ws.cell(35, 6, "Weekly profit times weeks per month."))

    label_cell(ws.cell(36, 1, "Profit per hour at that volume"))
    calc_cell(
        ws.cell(36, 2),
        'IF(OR(NOT(ISNUMBER(B34)),NOT(ISNUMBER(HoursWeekly)),HoursWeekly=0),"fill me in",B34/HoursWeekly)',
        fmt=CUR,
    )
    note_cell(ws.cell(36, 6, "Weekly profit divided by weekly hours from 05_Hours. This is a return on your time, not a wage."))
    ws.row_dimensions[36].height = 26

    label_cell(ws.cell(37, 1, "Break-even ticket at that volume"))
    calc_cell(
        ws.cell(37, 2),
        (
            'IF(OR(NOT(ISNUMBER(VariableUsed)),NOT(ISNUMBER(FixedWeekly)),NOT(ISNUMBER(B31)),B31=0),"fill me in",'
            'VariableUsed+FixedWeekly/B31)'
        ),
        fmt=CUR,
    )
    note_cell(ws.cell(37, 6, "The average ticket that would exactly cover costs at the scenario volume: V plus F divided by bowls per week."))
    ws.row_dimensions[37].height = 28

    header_bar(ws, 39, "F", "Plain-language readout")
    merge(
        ws,
        "A40:F41",
        (
            '=IF(NOT(ISNUMBER(B26)),'
            '"Fill the required yellow cells (ticket or mix, ingredients, packaging, selling days, and kitchen rate and hours, or 0 and 0 for kitchen) to see break-even bowls. Until then the model will not guess.",'
            'IF(B22<=0,'
            '"At the ticket and variable cost you entered, variable cost is at or above the ticket. There is no break-even at this price. Raise the ticket, change the mix, or lower variable cost.",'
            'CONCATENATE("At the ticket and costs you entered, you need ",TEXT(B26,"0.0"),'
            '" bowls per selling day (",TEXT(B25,"0.0")," per week) to cover cash costs. This is a break-even figure, not a living wage and not a forecast of demand.")'
            '))'
        ),
        font=font_label,
        fill=fill_cream,
        height=22,
    )
    ws.row_dimensions[40].height = 22
    ws.row_dimensions[41].height = 22
    # merge formula lives in A40; A41 is part of merge

    merge(
        ws,
        "A42:F43",
        (
            '=IF(NOT(ISNUMBER(B34)),'
            '"If you also type an optional scenario volume on 01_Operations_and_menu, this space will show weekly profit at that volume. If you also fill 05_Hours, it will show profit per hour.",'
            'CONCATENATE("At your optional scenario volume, weekly profit (no operator wage) is ",TEXT(B34,"$#,##0.00"),'
            'IF(ISNUMBER(B36),CONCATENATE(", which is ",TEXT(B36,"$#,##0.00")," per hour of the time you entered."),"."),'
            '" This is a scenario, not a forecast."))'
        ),
        font=font_label,
        fill=fill_cream,
    )
    ws.row_dimensions[42].height = 22
    ws.row_dimensions[43].height = 22

    header_bar(ws, 45, "F", "What was left blank (treated as $0)")
    label_cell(ws.cell(46, 1, "Omitted optional variable lines"))
    calc_cell(ws.cell(46, 2), "=IF(OmittedVariable=\"\",\"none\",OmittedVariable)")
    ws.merge_cells("B46:E46")
    note_cell(ws.cell(46, 6, "From 03_Packaging_and_fees."))
    ws.row_dimensions[46].height = 28
    label_cell(ws.cell(47, 1, "Omitted optional fixed lines"))
    calc_cell(ws.cell(47, 2), "=IF(OmittedFixed=\"\",\"none\",OmittedFixed)")
    ws.merge_cells("B47:E47")
    note_cell(ws.cell(47, 6, "From 04_Fixed_costs."))
    ws.row_dimensions[47].height = 28
    merge(
        ws,
        "A48:F48",
        "If those lists are not empty, the break-even figure is a partial cost picture. Fill the omitted lines, or enter 0 to confirm they do not apply, before treating the result as complete.",
        font=font_small,
        fill=fill_orange,
        height=28,
    )

    define(wb, "Contribution", ws.title, "$B$22")
    define(wb, "BEWeek", ws.title, "$B$25")
    define(wb, "BEDay", ws.title, "$B$26")
    define(wb, "BEMonth", ws.title, "$B$27")
    define(wb, "ScenWeekBowls", ws.title, "$B$31")
    define(wb, "WeeklyProfit", ws.title, "$B$34")
    define(wb, "ProfitPerHour", ws.title, "$B$36")

    # Conditional tint when a status cell says fill me in
    yellow_text = Font(name="Calibri", size=11, bold=True, color=YELLOW_DK)
    ws.conditional_formatting.add(
        "B6:B11",
        FormulaRule(formula=['ISNUMBER(B6)=FALSE'], fill=fill_yellow, font=yellow_text),
    )
    ws.conditional_formatting.add(
        "B14:B22",
        FormulaRule(formula=['ISNUMBER(B14)=FALSE'], fill=fill_yellow, font=yellow_text),
    )

    ws.freeze_panes = "A4"
    return ws




def build_income(wb):
    ws = wb.create_sheet("07_Income_target")
    apply_base(
        ws,
        {"A": 58, "B": 20, "C": 18, "D": 18, "E": 18, "F": 58},
        "C65D00",
        "Oats, Etc. Stage 1  |  Income-target scenario (secondary)",
    )
    merge(ws, "A1:F1", "07  Income-target scenario  |  SECONDARY VIEW ONLY", font_banner, fill=fill_orange, height=26)
    merge(
        ws,
        "A2:F3",
        "This tab is a scenario, not the purpose of Stage 1, and not a forecast. Stage 1 is a break-even experiment to learn from, not a living-wage plan. Costs still come from the other sheets. Type a target only if you want to see what volume, ticket, or schedule would leave that cash amount after the costs you entered.",
        font=font_label,
        fill=fill_orange,
        height=22,
    )
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[3].height = 22

    header_bar(ws, 5, "F", "Target  |  CHARLES FILLS THIS IN")
    col_headers(ws, 6, ["Input", "Value", "Unit", "", "", "Notes"])
    label_cell(ws.cell(7, 1, "Target weekly take-home"))
    input_cell(ws.cell(7, 2), fmt=CUR)
    paint(ws.cell(7, 3, "$ per week"), font=font_small, fill=fill_cream, align=center)
    for c in (4, 5):
        paint(ws.cell(7, c, ""), fill=fill_cream, border=True)
    note_cell(ws.cell(7, 6, "If both weekly and monthly are filled, the weekly target is used."))
    ws.row_dimensions[7].height = 24

    label_cell(ws.cell(8, 1, "Target monthly take-home"))
    input_cell(ws.cell(8, 2), fmt=CUR)
    paint(ws.cell(8, 3, "$ per month"), font=font_small, fill=fill_cream, align=center)
    for c in (4, 5):
        paint(ws.cell(8, c, ""), fill=fill_cream, border=True)
    note_cell(ws.cell(8, 6, "Used only if the weekly target is blank: weekly target = monthly divided by weeks per month."))
    ws.row_dimensions[8].height = 24

    label_cell(ws.cell(9, 1, "Weekly target used in this scenario"))
    calc_cell(
        ws.cell(9, 2),
        'IF(ISNUMBER(B7),B7,IF(AND(ISNUMBER(B8),ISNUMBER(WeeksPerMonth),WeeksPerMonth<>0),B8/WeeksPerMonth,"fill me in"))',
        fmt=CUR,
    )
    note_cell(ws.cell(9, 6, "SCENARIO input, converted to a weekly cash amount."))
    for c in (3, 4, 5):
        paint(ws.cell(9, c, ""), fill=fill_green, border=True)

    header_bar(ws, 11, "F", "Scenario outputs  (same costs as the break-even tab)")
    label_cell(ws.cell(12, 1, "Contribution per bowl (C)"))
    calc_cell(ws.cell(12, 2), '=IF(ISNUMBER(Contribution),Contribution,"fill me in")', fmt=CUR)
    note_cell(ws.cell(12, 6, "From 06_Break_even."))

    label_cell(ws.cell(13, 1, "Weekly fixed cost (F)"))
    calc_cell(ws.cell(13, 2), '=IF(ISNUMBER(FixedWeekly),FixedWeekly,"fill me in")', fmt=CUR)
    note_cell(ws.cell(13, 6, "From 04_Fixed_costs."))

    label_cell(ws.cell(14, 1, "SCENARIO: bowls per week to hit the target"))
    calc_cell(
        ws.cell(14, 2),
        (
            'IF(OR(NOT(ISNUMBER(B9)),NOT(ISNUMBER(B13)),NOT(ISNUMBER(B12))),"fill me in",'
            'IF(B12<=0,"ticket must be higher than variable cost",(B13+B9)/B12))'
        ),
        fmt=NUM1,
    )
    note_cell(ws.cell(14, 6, "(Weekly fixed cost plus target weekly income) divided by contribution per bowl."))
    ws.row_dimensions[14].height = 28

    label_cell(ws.cell(15, 1, "SCENARIO: bowls per selling day to hit the target"))
    calc_cell(
        ws.cell(15, 2),
        'IF(OR(NOT(ISNUMBER(B14)),NOT(ISNUMBER(SellingDays)),SellingDays=0),"fill me in",B14/SellingDays)',
        fmt=NUM1,
    )
    note_cell(ws.cell(15, 6, "The weekly figure divided by selling days per week."))

    label_cell(ws.cell(16, 1, "SCENARIO: ticket needed at the optional scenario volume"))
    calc_cell(
        ws.cell(16, 2),
        (
            'IF(OR(NOT(ISNUMBER(VariableUsed)),NOT(ISNUMBER(B13)),NOT(ISNUMBER(B9)),NOT(ISNUMBER(ScenWeekBowls)),ScenWeekBowls=0),"fill me in",'
            'VariableUsed+(B13+B9)/ScenWeekBowls)'
        ),
        fmt=CUR,
    )
    note_cell(ws.cell(16, 6, "Variable cost plus (fixed plus target) divided by scenario bowls per week. Requires the optional volume on 01_Operations_and_menu."))
    ws.row_dimensions[16].height = 32

    label_cell(ws.cell(17, 1, "SCENARIO: selling days per week needed at the optional daily volume and current ticket"))
    # F = KitchenPerDay * D + OtherFixedWeek_that_is_not_per_day_already... this is messy because OtherFixedWeek already includes per-day items * current D.
    # I need a clean split: per-day costs vs costs that do not change with D.
    # KitchenPerDay is a number. Fuel may be per selling day and is inside OtherFixedWeek.
    # Honest approach: if I don't have a clean split of other fixed into per-day vs not, I shouldn't invent a days-needed formula that treats all F as independent of D.
    # I'll compute:
    # Let PD = KitchenPerDay + fuel if fuel is per selling day... too coupled.
    # Simpler honest formula:
    # Profit per selling day at volume Q = C*Q - (F_week / current_D)  is WRONG if some costs are monthly.
    # Correct:
    # Weekly profit = C*Q*D - (PerDayCosts * D + NonDayWeekly)
    # Set equal to target I: C*Q*D - PerDay*D - NonDay = I
    # D * (C*Q - PerDay) = I + NonDay
    # D = (I + NonDay) / (C*Q - PerDay)
    # I need NonDay weekly and PerDay.
    # KitchenPerDay is known. OtherFixedWeek mixes frequencies already converted using current SellingDays.
    # I could named-range the per-selling-day other costs * 1 day...
    # From sheet 04: F15 is weekly amount for fuel (if per selling day, F15 = B15*SellingDays, so per day = F15/SellingDays if selling days filled)
    # Actually any "per selling day" row's weekly amount / SellingDays = the daily amount.
    # Easier: add two named calcs on sheet 04... I didn't. 
    # I'll explain in the note that this uses: per-day cost = KitchenPerDay plus (weekly fixed - kitchen per week) only when... no that's wrong for monthly costs.
    #
    # Per-day costs total = KitchenPerDay + (sum of other costs with frequency per selling day).
    # I can compute from 04_Fixed_costs! 
    # Fuel weekly F15 / SellingDays if C15 is per selling day.
    # I'll add a helper on this sheet that references 04:
    # PerDayOther = IF(ISNUMBER(SellingDays), 
    #   (IF('04_Fixed_costs'!C15="per selling day",'04_Fixed_costs'!B15,0)+... ), fill me in)
    # That's clean.

    calc_cell(
        ws.cell(17, 2),
        (
            'IF(OR(NOT(ISNUMBER(B9)),NOT(ISNUMBER(Contribution)),NOT(ISNUMBER(ScenarioBowls)),'
            'NOT(ISNUMBER(KitchenPerDay)),NOT(ISNUMBER(SellingDays)),NOT(ISNUMBER(FixedWeekly))),"fill me in",'
            'IF((Contribution*ScenarioBowls-B18)<=0,"contribution per day does not cover per-day costs plus a target at this volume",'
            '(B9+B19)/B20))'
        ),
        fmt=NUM1,
    )
    # Wait I'm referencing B18, B19, B20 which I'll put as helpers below. Let me reorder: helpers first, then this result.
    # I'll put helpers in rows 19-21 and result stays... let me change plan:
    # Row 17 label stays, but I'll put helpers at 19-21 and formula of 17 will be written after I define helpers... I'm appending formula now incorrectly.
    # I'll overwrite cell 17 formula after helpers, or put the days-needed result in row 22.
    # Let me put helpers in 19-21 and move days-needed to 22. I'll clear 17 to a pointer.

    # Actually let me just write helpers now at 19-21 and fix 17 to a short note, result at 22.
    ws["A17"].value = "See row 22 for selling days needed. Helper amounts are in rows 19 to 21."
    ws["B17"].value = ""
    paint(ws["B17"], font=font_small, fill=fill_cream, border=True)
    note_cell(ws.cell(17, 6, "Helpers compute per-day costs versus costs that do not change with the number of selling days."))
    ws.row_dimensions[17].height = 28

    header_bar(ws, 19, "F", "Helpers for the selling-days scenario")
    label_cell(ws.cell(20, 1, "Other costs that are billed per selling day (sum of amounts)"))
    calc_cell(
        ws.cell(20, 2),
        (
            'IF(\'04_Fixed_costs\'!C15="per selling day",IF(ISNUMBER(\'04_Fixed_costs\'!B15),\'04_Fixed_costs\'!B15,0),0)'
            '+IF(\'04_Fixed_costs\'!C16="per selling day",IF(ISNUMBER(\'04_Fixed_costs\'!B16),\'04_Fixed_costs\'!B16,0),0)'
            '+IF(\'04_Fixed_costs\'!C17="per selling day",IF(ISNUMBER(\'04_Fixed_costs\'!B17),\'04_Fixed_costs\'!B17,0),0)'
            '+IF(\'04_Fixed_costs\'!C18="per selling day",IF(ISNUMBER(\'04_Fixed_costs\'!B18),\'04_Fixed_costs\'!B18,0),0)'
            '+IF(\'04_Fixed_costs\'!C19="per selling day",IF(ISNUMBER(\'04_Fixed_costs\'!B19),\'04_Fixed_costs\'!B19,0),0)'
            '+IF(\'04_Fixed_costs\'!C20="per selling day",IF(ISNUMBER(\'04_Fixed_costs\'!B20),\'04_Fixed_costs\'!B20,0),0)'
            '+IF(\'04_Fixed_costs\'!C21="per selling day",IF(ISNUMBER(\'04_Fixed_costs\'!B21),\'04_Fixed_costs\'!B21,0),0)'
            '+IF(\'04_Fixed_costs\'!C22="per selling day",IF(ISNUMBER(\'04_Fixed_costs\'!B22),\'04_Fixed_costs\'!B22,0),0)'
            '+IF(\'04_Fixed_costs\'!C23="per selling day",IF(ISNUMBER(\'04_Fixed_costs\'!B23),\'04_Fixed_costs\'!B23,0),0)'
        ),
        fmt=CUR,
    )
    note_cell(ws.cell(20, 6, "Amounts from 04_Fixed_costs whose frequency is per selling day. Kitchen is added separately."))
    ws.row_dimensions[20].height = 28

    label_cell(ws.cell(21, 1, "Total cost per selling day (kitchen plus other per-day costs)"))
    calc_cell(
        ws.cell(21, 2),
        'IF(NOT(ISNUMBER(KitchenPerDay)),"fill me in",KitchenPerDay+IF(ISNUMBER(B20),B20,0))',
        fmt=CUR,
    )
    note_cell(ws.cell(21, 6, "These costs rise when you add a selling morning."))

    label_cell(ws.cell(22, 1, "Weekly costs that do not change with selling days"))
    calc_cell(
        ws.cell(22, 2),
        (
            'IF(OR(NOT(ISNUMBER(FixedWeekly)),NOT(ISNUMBER(SellingDays)),NOT(ISNUMBER(B21))),"fill me in",'
            'FixedWeekly-B21*SellingDays)'
        ),
        fmt=CUR,
    )
    note_cell(ws.cell(22, 6, "Weekly fixed cost minus (per-day cost times the current selling days). This should equal the monthly and yearly items, plus weekly items, plus any startup recovery."))
    ws.row_dimensions[22].height = 32

    label_cell(ws.cell(23, 1, "SCENARIO: selling days per week needed at the optional daily volume and current ticket"))
    calc_cell(
        ws.cell(23, 2),
        (
            'IF(OR(NOT(ISNUMBER(B9)),NOT(ISNUMBER(Contribution)),NOT(ISNUMBER(ScenarioBowls)),'
            'NOT(ISNUMBER(B21)),NOT(ISNUMBER(B22))),"fill me in",'
            'IF((Contribution*ScenarioBowls-B21)<=0,"contribution per day does not cover per-day costs plus a target at this volume",'
            '(B9+B22)/(Contribution*ScenarioBowls-B21)))'
        ),
        fmt=NUM1,
    )
    note_cell(ws.cell(23, 6, "(Target plus non-day weekly costs) divided by (contribution per day minus cost per selling day). Requires the optional scenario volume."))
    ws.row_dimensions[23].height = 36

    merge(
        ws,
        "A25:F26",
        (
            '=IF(NOT(ISNUMBER(B15)),'
            '"This is a secondary scenario. Fill a target and the same required costs as the break-even tab to see the bowls that would leave that cash amount.",'
            'CONCATENATE("SCENARIO ONLY. To leave ",TEXT(B9,"$#,##0.00")," per week after the costs you entered, you would need ",'
            'TEXT(B15,"0.0")," bowls per selling day (",TEXT(B14,"0.0")," per week). This is not a Stage 1 goal and not a forecast."))'
        ),
        font=font_label,
        fill=fill_orange,
    )
    ws.row_dimensions[25].height = 22
    ws.row_dimensions[26].height = 22

    define(wb, "TargetWeekly", ws.title, "$B$9")
    ws.freeze_panes = "A5"
    return ws


def build_sensitivity(wb):
    ws = wb.create_sheet("08_Sensitivity")
    apply_base(
        ws,
        {"A": 46, "B": 20, "C": 22, "D": 22, "E": 22, "F": 50},
        "3D8B6E",
        "Oats, Etc. Stage 1  |  Sensitivity",
    )
    merge(ws, "A1:F1", "08  Which inputs move break-even most", font_title, height=24)
    merge(
        ws,
        "A2:F4",
        (
            "Break-even bowls per week equal weekly fixed cost (F) divided by contribution per bowl (C = ticket minus variable cost). "
            "Because C is the divisor, ticket and variable cost move the answer most when the margin is thin. "
            "A mix that leans on the $5.95 Classic, or an average ticket that assumed add-ons that customers do not buy, shrinks C. "
            "Kitchen rental is likely the largest cost that repeats every selling morning. "
            "Insurance and licenses hurt more per morning if you sell fewer days per week. "
            "Hours worked do not change break-even bowls. They change profit per hour once a volume is entered. "
            "The tables below stay on fill me in until required costs and a ticket are filled. The Classic-only case is included because the archive's $7.50 Stage 1 average is a model input, not a measured mix (notes/oe-challenger/adversarial-review-round-2-2026-11-11.md, objection 3, read only)."
        ),
        font=font_label,
        fill=fill_cream,
    )
    for r in (2, 3, 4):
        ws.row_dimensions[r].height = 22

    # Helper: BE week given T, V, F
    # = IF(any missing, fill me in, if T-V<=0, "no BE", F/(T-V))
    def be_formula(t, v, f):
        return (
            f'IF(OR(NOT(ISNUMBER({t})),NOT(ISNUMBER({v})),NOT(ISNUMBER({f}))),"fill me in",'
            f'IF(({t})-({v})<=0,"ticket must be higher than variable cost",({f})/(({t})-({v}))))'
        )

    header_bar(ws, 6, "F", "Base values from the model")
    label_cell(ws.cell(7, 1, "Base ticket (T)"))
    calc_cell(ws.cell(7, 2), '=IF(ISNUMBER(TicketUsed),TicketUsed,"fill me in")', fmt=CUR)
    label_cell(ws.cell(8, 1, "Base variable cost (V)"))
    calc_cell(ws.cell(8, 2), '=IF(ISNUMBER(VariableUsed),VariableUsed,"fill me in")', fmt=CUR)
    label_cell(ws.cell(9, 1, "Base weekly fixed cost (F)"))
    calc_cell(ws.cell(9, 2), '=IF(ISNUMBER(FixedWeekly),FixedWeekly,"fill me in")', fmt=CUR)
    label_cell(ws.cell(10, 1, "Base break-even bowls per week"))
    calc_cell(ws.cell(10, 2), '=IF(ISNUMBER(BEWeek),BEWeek,"fill me in")', fmt=NUM1)
    label_cell(ws.cell(11, 1, "Classic proposed price (cited assumption)"))
    calc_cell(ws.cell(11, 2), '=IF(ISNUMBER(ClassicPrice),ClassicPrice,"fill me in")', fmt=CUR)
    note_cell(ws.cell(11, 6, "From 01_Operations_and_menu, default $5.95 from pilot-and-equipment.md."))
    for r in range(7, 12):
        for c in (3, 4, 5):
            paint(ws.cell(r, c, ""), fill=fill_green, border=True)
        if r != 11:
            note_cell(ws.cell(r, 6, ""))
        ws.row_dimensions[r].height = 20

    header_bar(ws, 13, "F", "Average ticket cases  (variable cost and weekly fixed cost held at base)")
    col_headers(ws, 14, ["Case", "Ticket", "Break-even bowls / week", "Change vs base", "Bowls / selling day", "Notes"])
    ticket_cases = [
        (15, "Ticket minus $1.50", "=IF(ISNUMBER($B$7),$B$7-1.5,\"fill me in\")", ""),
        (16, "Ticket minus $1.00", "=IF(ISNUMBER($B$7),$B$7-1,\"fill me in\")", ""),
        (17, "Ticket minus $0.50", "=IF(ISNUMBER($B$7),$B$7-0.5,\"fill me in\")", ""),
        (18, "Base ticket", "=IF(ISNUMBER($B$7),$B$7,\"fill me in\")", "Current model ticket."),
        (19, "Ticket plus $0.50", "=IF(ISNUMBER($B$7),$B$7+0.5,\"fill me in\")", ""),
        (20, "Ticket plus $1.00", "=IF(ISNUMBER($B$7),$B$7+1,\"fill me in\")", ""),
        (21, "Ticket plus $1.50", "=IF(ISNUMBER($B$7),$B$7+1.5,\"fill me in\")", ""),
        (22, "Classic only, no add-on ($5.95 unless you edited the Classic price)", "=IF(ISNUMBER($B$11),$B$11,\"fill me in\")", "Stress case: everyone buys the Classic with no add-on. See Challenger round 2, objection 3."),
    ]
    for r, name, t_formula, notes in ticket_cases:
        label_cell(ws.cell(r, 1, name))
        calc_cell(ws.cell(r, 2), t_formula, fmt=CUR)
        calc_cell(ws.cell(r, 3), "=" + be_formula(f"B{r}", "$B$8", "$B$9"), fmt=NUM1)
        calc_cell(
            ws.cell(r, 4),
            f'IF(OR(NOT(ISNUMBER(C{r})),NOT(ISNUMBER($B$10))),"fill me in",C{r}-$B$10)',
            fmt=NUM1,
        )
        calc_cell(
            ws.cell(r, 5),
            f'IF(OR(NOT(ISNUMBER(C{r})),NOT(ISNUMBER(SellingDays)),SellingDays=0),"fill me in",C{r}/SellingDays)',
            fmt=NUM1,
        )
        note_cell(ws.cell(r, 6, notes))
        ws.row_dimensions[r].height = 22 if r < 22 else 32

    header_bar(ws, 24, "F", "Variable cost cases  (ticket and weekly fixed cost held at base)")
    col_headers(ws, 25, ["Case", "Variable cost", "Break-even bowls / week", "Change vs base", "Bowls / selling day", "Notes"])
    var_cases = [
        (26, "Variable cost minus 20%", 0.80),
        (27, "Variable cost minus 10%", 0.90),
        (28, "Base variable cost", 1.00),
        (29, "Variable cost plus 10%", 1.10),
        (30, "Variable cost plus 20%", 1.20),
        (31, "Variable cost plus 30%", 1.30),
    ]
    for r, name, mult in var_cases:
        label_cell(ws.cell(r, 1, name))
        calc_cell(ws.cell(r, 2), f'=IF(ISNUMBER($B$8),$B$8*{mult},"fill me in")', fmt=CUR)
        calc_cell(ws.cell(r, 3), "=" + be_formula("$B$7", f"B{r}", "$B$9"), fmt=NUM1)
        calc_cell(ws.cell(r, 4), f'IF(OR(NOT(ISNUMBER(C{r})),NOT(ISNUMBER($B$10))),"fill me in",C{r}-$B$10)', fmt=NUM1)
        calc_cell(ws.cell(r, 5), f'IF(OR(NOT(ISNUMBER(C{r})),NOT(ISNUMBER(SellingDays)),SellingDays=0),"fill me in",C{r}/SellingDays)', fmt=NUM1)
        note_cell(ws.cell(r, 6, ""))
        ws.row_dimensions[r].height = 20

    header_bar(ws, 33, "F", "Weekly fixed cost cases  (ticket and variable cost held at base)")
    col_headers(ws, 34, ["Case", "Weekly fixed cost", "Break-even bowls / week", "Change vs base", "Bowls / selling day", "Notes"])
    fix_cases = [
        (35, "Weekly fixed minus 50%", 0.50),
        (36, "Weekly fixed minus 20%", 0.80),
        (37, "Base weekly fixed cost", 1.00),
        (38, "Weekly fixed plus 20%", 1.20),
        (39, "Weekly fixed plus 50%", 1.50),
    ]
    for r, name, mult in fix_cases:
        label_cell(ws.cell(r, 1, name))
        calc_cell(ws.cell(r, 2), f'=IF(ISNUMBER($B$9),$B$9*{mult},"fill me in")', fmt=CUR)
        calc_cell(ws.cell(r, 3), "=" + be_formula("$B$7", "$B$8", f"B{r}"), fmt=NUM1)
        calc_cell(ws.cell(r, 4), f'IF(OR(NOT(ISNUMBER(C{r})),NOT(ISNUMBER($B$10))),"fill me in",C{r}-$B$10)', fmt=NUM1)
        calc_cell(ws.cell(r, 5), f'IF(OR(NOT(ISNUMBER(C{r})),NOT(ISNUMBER(SellingDays)),SellingDays=0),"fill me in",C{r}/SellingDays)', fmt=NUM1)
        note_cell(ws.cell(r, 6, "Kitchen hours and the hourly rate are the usual way a small experiment changes F."))
        ws.row_dimensions[r].height = 22

    header_bar(ws, 41, "F", "Selling days per week  (2, 3, 4, or 5 mornings)")
    col_headers(ws, 42, ["Selling days / week", "Weekly fixed cost at that schedule", "Break-even bowls / week", "Break-even bowls / selling day", "", "Notes"])
    # Weekly F at a different D: F = KitchenPerDay*D + (FixedWeekly - KitchenPerDay*SellingDays)
    # More correctly: F_new = PerDayTotal * D_new + NonDayWeekly
    # I can use 07 helpers? Better compute here from named ranges.
    # NonDay = FixedWeekly - KitchenPerDay*SellingDays - OtherPerDay*SellingDays
    # I didn't name OtherPerDay. I can use the same sum as income sheet, or approximate with Kitchen only for a note...
    # Honest: weekly fixed at new D = FixedWeekly - KitchenPerDay*SellingDays + KitchenPerDay*newD, PLUS adjustment for other per-day costs.
    # I'll pull the same per-day other sum as sheet 07 B20... that's a bit coupled. Duplicate the short version: reference 07_Income_target!B20 and B21.
    # PerDay = '07_Income_target'!B21
    # NonDay = '07_Income_target'!B22  -- BUT B22 uses current SellingDays, which is correct (NonDay doesn't change with D).
    # F_new = PerDay * newD + NonDay
    # This works once kitchen is filled (B21 needs KitchenPerDay).

    for i, days in enumerate((2, 3, 4, 5)):
        r = 43 + i
        label_cell(ws.cell(r, 1, days))
        ws.cell(r, 1).number_format = "0"
        paint(ws.cell(r, 1), font=font_label, fill=fill_gray, align=center)
        calc_cell(
            ws.cell(r, 2),
            (
                f'IF(OR(NOT(ISNUMBER(\'07_Income_target\'!B21)),NOT(ISNUMBER(\'07_Income_target\'!B22))),"fill me in",'
                f'\'07_Income_target\'!B21*{days}+\'07_Income_target\'!B22)'
            ),
            fmt=CUR,
        )
        calc_cell(ws.cell(r, 3), "=" + be_formula("$B$7", "$B$8", f"B{r}"), fmt=NUM1)
        calc_cell(
            ws.cell(r, 4),
            f'IF(NOT(ISNUMBER(C{r})),"fill me in",C{r}/{days})',
            fmt=NUM1,
        )
        paint(ws.cell(r, 5, ""), fill=fill_green, border=True)
        note_cell(ws.cell(r, 6, "Per-day costs (kitchen and any other per-day lines) scale with mornings. Monthly licenses and insurance do not."))
        ws.row_dimensions[r].height = 24

    header_bar(ws, 48, "F", "Top mover among a 10 percent change in ticket, variable cost, or weekly fixed cost")
    label_cell(ws.cell(49, 1, "Break-even bowls / week if ticket is 10% higher"))
    calc_cell(ws.cell(49, 2), "=" + be_formula("$B$7*1.1", "$B$8", "$B$9"), fmt=NUM1)
    calc_cell(ws.cell(49, 3), '=IF(OR(NOT(ISNUMBER(B49)),NOT(ISNUMBER($B$10))),"fill me in",B49-$B$10)', fmt=NUM1)
    note_cell(ws.cell(49, 6, "Change in weekly break-even bowls (usually a decrease)."))

    label_cell(ws.cell(50, 1, "Break-even bowls / week if variable cost is 10% higher"))
    calc_cell(ws.cell(50, 2), "=" + be_formula("$B$7", "$B$8*1.1", "$B$9"), fmt=NUM1)
    calc_cell(ws.cell(50, 3), '=IF(OR(NOT(ISNUMBER(B50)),NOT(ISNUMBER($B$10))),"fill me in",B50-$B$10)', fmt=NUM1)
    note_cell(ws.cell(50, 6, "Change in weekly break-even bowls (usually an increase)."))

    label_cell(ws.cell(51, 1, "Break-even bowls / week if weekly fixed cost is 10% higher"))
    calc_cell(ws.cell(51, 2), "=" + be_formula("$B$7", "$B$8", "$B$9*1.1"), fmt=NUM1)
    calc_cell(ws.cell(51, 3), '=IF(OR(NOT(ISNUMBER(B51)),NOT(ISNUMBER($B$10))),"fill me in",B51-$B$10)', fmt=NUM1)
    note_cell(ws.cell(51, 6, "Change in weekly break-even bowls (usually an increase)."))

    label_cell(ws.cell(52, 1, "Largest move among those three (by absolute change in bowls)"))
    calc_cell(
        ws.cell(52, 2),
        (
            'IF(OR(NOT(ISNUMBER(C49)),NOT(ISNUMBER(C50)),NOT(ISNUMBER(C51))),"fill me in",'
            'IF(AND(ABS(C49)>=ABS(C50),ABS(C49)>=ABS(C51)),"ticket (10% higher)",'
            'IF(ABS(C50)>=ABS(C51),"variable cost (10% higher)","weekly fixed cost (10% higher)")))'
        ),
    )
    note_cell(ws.cell(52, 6, "This compares equal 10% shocks. A thin contribution still means ticket and variable cost are the usual first place to look, even if a large kitchen bill also matters in dollars."))
    ws.merge_cells("B52:C52")
    ws.row_dimensions[52].height = 36

    for r in (49, 50, 51):
        for c in (4, 5):
            paint(ws.cell(r, c, ""), fill=fill_green, border=True)
        label_cell(ws.cell(r, 4)) if False else None
        ws.row_dimensions[r].height = 22

    ws.freeze_panes = "A6"
    return ws




def build_example(wb):
    ws = wb.create_sheet("09_Example_only")
    apply_base(
        ws,
        {"A": 42, "B": 16, "C": 16, "D": 16, "E": 16, "F": 16, "G": 16, "H": 48},
        "C65D00",
        "Oats, Etc. Stage 1  |  EXAMPLE ONLY",
    )
    merge(
        ws,
        "A1:H1",
        "09  EXAMPLE ONLY  |  not your costs, not a forecast, not a complete break-even",
        font_banner,
        fill=fill_orange,
        height=26,
    )
    merge(
        ws,
        "A2:H4",
        (
            "This tab walks through kitchen-only math using figures already published as illustrations in the research archive. "
            "Ingredient and packaging costs are still unknown, so they are excluded here, not assumed to be zero. "
            "Real break-even will be higher once food, packaging, and other costs are included. "
            "This example also does not guess your prep, travel, or cleaning time, so it does not report profit per hour. "
            "Do not copy these figures into the yellow cells of the real template unless a cited source is actually the confirmed number you mean to use."
        ),
        font=font_label,
        fill=fill_orange,
    )
    for r in (2, 3, 4):
        ws.row_dimensions[r].height = 20

    header_bar(ws, 6, "H", "Cited example inputs  (every figure has a source; none is a measured cost from a receipt)")
    col_headers(ws, 7, ["Input", "Example value", "Unit", "", "", "", "", "Source (this is an assumption or illustration, not a confirmed quote)"])

    examples = [
        (8, "EXAMPLE ticket: Stage 1 table average", 7.50, CUR, "$ per bowl", "docs/oats-and-more/research/pilot-and-equipment.md, Stage 1 model input. Not a measured average ticket."),
        (9, "EXAMPLE ticket: Classic, no add-on", 5.95, CUR, "$ per bowl", "Starter menu working price in the same file. Used as a stress case in notes/oe-challenger/adversarial-review-round-2-2026-11-11.md, objection 3."),
        (10, "EXAMPLE ticket: kitchen-memo illustrative check", 9.00, CUR, "$ per bowl", "docs/oats-and-more/research/boise-kitchen-and-office-service-market-2026-11-11.md, illustrative gross-sales check."),
        (11, "EXAMPLE kitchen hours per selling morning", 2, NUM1, "hours", "Same kitchen memo, illustrative check. Not a booking."),
        (12, "EXAMPLE advertised kitchen rate, lower listing", 30, CUR, "$ per hour", "Advertised Flava Kitchen list rate in that memo. Not a reservation, and a four-hour session may apply."),
        (13, "EXAMPLE advertised kitchen rate, higher listing", 40, CUR, "$ per hour", "Advertised Gina's Kitchen list rate, and Commons prime rate, in that memo. Not a reservation."),
        (14, "EXAMPLE selling days per week (Stage 1 table)", 3, NUM1, "days", "docs/oats-and-more/research/pilot-and-equipment.md, Stage 1 table. The decision log still lists days per week as not decided."),
        (15, "EXAMPLE weeks per month", 4.33, "0.00", "weeks", "Same file, monthly math note."),
        (16, "EXAMPLE variable cost per bowl", 0, CUR, "$ per bowl", "EXCLUDED, not claimed to be zero. Ingredients, packaging, fees, fuel, licenses, insurance, and every other non-kitchen cost are left out of this example."),
    ]
    for r, lab, val, fmt, unit, src in examples:
        paint(ws.cell(r, 1, lab), font=font_warn, fill=fill_orange, align=wrap_left)
        c = paint(ws.cell(r, 2, val), font=font_warn, fill=fill_orange, align=center, fmt=fmt)
        paint(ws.cell(r, 3, unit), font=font_small, fill=fill_orange, align=center)
        for col in (4, 5, 6, 7):
            paint(ws.cell(r, col, ""), fill=fill_orange, border=True)
        note_cell(ws.cell(r, 8, src))
        ws.cell(r, 8).fill = fill_orange
        ws.row_dimensions[r].height = 32

    header_bar(ws, 18, "H", "EXAMPLE kitchen cost per selling morning  (rate times 2 hours)")
    label_cell(ws.cell(19, 1, "EXAMPLE kitchen cost at $30 per hour"))
    calc_cell(ws.cell(19, 2), "=B12*B11", fmt=CUR)
    note_cell(ws.cell(19, 8, "30 times 2 = 60, matching the kitchen memo table."))
    label_cell(ws.cell(20, 1, "EXAMPLE kitchen cost at $40 per hour"))
    calc_cell(ws.cell(20, 2), "=B13*B11", fmt=CUR)
    note_cell(ws.cell(20, 8, "40 times 2 = 80, matching the kitchen memo table."))
    for r in (19, 20):
        for c in range(3, 8):
            paint(ws.cell(r, c, ""), fill=fill_green, border=True)
        ws.cell(r, 1).fill = fill_orange
        ws.cell(r, 1).font = font_warn

    header_bar(ws, 22, "H", "EXAMPLE kitchen-only break-even bowls per selling morning  (kitchen cost divided by ticket, because variable cost is excluded)")
    col_headers(ws, 23, ["Ticket used", "BE bowls at $30/hr kitchen", "BE bowls at $40/hr kitchen", "", "", "", "", "How to read this"])
    be_rows = [
        (24, "=$B$8", "Stage 1 table ticket $7.50"),
        (25, "=$B$9", "Classic only $5.95, no add-on"),
        (26, "=$B$10", "Kitchen-memo illustrative ticket $9.00"),
    ]
    for r, tref, note in be_rows:
        calc_cell(ws.cell(r, 1), tref, fmt=CUR)
        calc_cell(
            ws.cell(r, 2),
            f'IF(A{r}-$B$16<=0,"ticket must be higher than variable cost",$B$19/(A{r}-$B$16))',
            fmt=NUM1,
        )
        calc_cell(
            ws.cell(r, 3),
            f'IF(A{r}-$B$16<=0,"ticket must be higher than variable cost",$B$20/(A{r}-$B$16))',
            fmt=NUM1,
        )
        for c in range(4, 8):
            paint(ws.cell(r, c, ""), fill=fill_green, border=True)
        note_cell(ws.cell(r, 8, note + ". This is a floor. Adding food and packaging will raise these counts."))
        ws.row_dimensions[r].height = 28

    header_bar(ws, 28, "H", "EXAMPLE gross sales and kitchen share of gross  (reproduces the kitchen memo's illustrative table, plus the Stage 1 monthly math)")
    col_headers(
        ws,
        29,
        [
            "Bowls in one morning",
            "Gross at $7.50",
            "Gross at $9.00",
            "$30/hr kitchen as % of $9 gross",
            "$40/hr kitchen as % of $9 gross",
            "Monthly gross at $7.50, 3 days, 4.33 weeks",
            "",
            "Notes",
        ],
    )
    volumes = [20, 30, 35, 40, 50, 60]
    for i, q in enumerate(volumes):
        r = 30 + i
        paint(ws.cell(r, 1, q), font=font_warn, fill=fill_orange, align=center, fmt="0")
        calc_cell(ws.cell(r, 2), f"=A{r}*$B$8", fmt=CUR)
        calc_cell(ws.cell(r, 3), f"=A{r}*$B$10", fmt=CUR)
        calc_cell(ws.cell(r, 4), f'=IF(C{r}=0,"",$B$19/C{r})', fmt="0.0%")
        calc_cell(ws.cell(r, 5), f'=IF(C{r}=0,"",$B$20/C{r})', fmt="0.0%")
        calc_cell(ws.cell(r, 6), f"=A{r}*$B$8*$B$14*$B$15", fmt=CUR)
        paint(ws.cell(r, 7, ""), fill=fill_green, border=True)
        if q in (20, 35):
            note = "Stage 1 table in pilot-and-equipment.md uses 20 to 35 bowls and $7.50. Monthly math there rounds to $1,949 to $3,410."
        elif q in (30, 60):
            note = "Working hypothesis of 30 to 60 paid bowls is in docs/oats-and-more/README.md and validation-backlog.md. Hypothesis only."
        else:
            note = "Volume is an illustration from the kitchen memo table, not a forecast."
        note_cell(ws.cell(r, 8, note))
        ws.row_dimensions[r].height = 28

    merge(
        ws,
        "A37:H39",
        (
            "How to use this example: it shows why a 10 to 15 bowl morning can be eaten up by kitchen rent alone, which is the point already made in "
            "docs/oats-and-more/research/boise-kitchen-and-office-service-market-2026-11-11.md. "
            "At a $9 ticket and 20 bowls, the $60 kitchen bill is 33% of gross and the $80 kitchen bill is 44% of gross, matching that memo, before any food or packaging. "
            "Fill the yellow cells on the other tabs from receipts and quotes to see a complete break-even. "
            "If your variable cost is X dollars, kitchen-only break-even no longer applies; the real figure is weekly fixed cost divided by (ticket minus X)."
        ),
        font=font_label,
        fill=fill_orange,
    )
    for r in (37, 38, 39):
        ws.row_dimensions[r].height = 22

    ws.freeze_panes = "A6"
    return ws


def build_sources(wb):
    ws = wb.create_sheet("10_Sources_and_formulas")
    apply_base(
        ws,
        {"A": 36, "B": 36, "C": 28, "D": 80},
        "555555",
        "Oats, Etc. Stage 1  |  Sources and formulas",
    )
    merge(ws, "A1:D1", "10  Cited assumptions, file paths, and formulas", font_title, height=24)
    merge(
        ws,
        "A2:D2",
        "Paths are relative to the root of cwarloe/businessideas. OE Growth Steward notes in pull request 3 were read only and were not modified. The longer source write-up is assumptions-and-sources.md.",
        font=font_small,
        fill=fill_cream,
        height=28,
    )

    header_bar(ws, 4, "D", "Assumptions used in this workbook")
    col_headers(ws, 5, ["Topic", "What was assumed", "Pre-filled in the model?", "Source"])
    sources = [
        (
            "Stage 1 purpose",
            "A break-even experiment to learn from, not a living-wage plan. Gross sales are not profit. One operator, no paid staff in the archive sketches.",
            "Yes, as labels and structure, not as a number.",
            "docs/oats-and-more/research/README.md; docs/oats-and-more/research/decision-log.md; notes/oe-challenger/adversarial-review-round-2-2026-11-11.md",
        ),
        (
            "Menu",
            "Breakfast first, one plain oatmeal base, three starter bowls, no egg on the initial menu.",
            "Yes, as bowl names on the ingredient and mix sheets.",
            "docs/oats-and-more/research/decision-log.md; docs/oats-and-more/research/pilot-and-equipment.md; docs/oats-and-more/README.md",
        ),
        (
            "Proposed prices",
            "Classic $5.95, Maple Walnut $7.50, Apple Pie Oats $7.95. Working price points, not tested prices.",
            "Yes, as editable assumptions on 01_Operations_and_menu. Not copied into the average-ticket cell.",
            "docs/oats-and-more/research/pilot-and-equipment.md",
        ),
        (
            "Public-site menu",
            "The concept site lists a broader menu and some different add-on prices, all labeled test or illustrative. That site is not the Stage 1 default mix.",
            "No. Recorded in assumptions-and-sources.md only, so the two menus are not confused.",
            "docs/oats-and-more/index.html; docs/oats-and-more/menu-board.html",
        ),
        (
            "Morning window",
            "About 6:30 to 9:30 a.m., about three hours. Site hypothesis, not a confirmed host schedule.",
            "No. Service-hour cells are blank. Notes tell you to enter 3 if that window is yours.",
            "docs/oats-and-more/research/decision-log.md; validation-backlog.md; local-regulation.md",
        ),
        (
            "Days per week",
            "Not decided (2, 3, 4, or 5). The Stage 1 table uses 3 as a model input.",
            "No, left blank. The example tab uses 3 and labels it an example.",
            "docs/oats-and-more/research/decision-log.md; pilot-and-equipment.md",
        ),
        (
            "Volume hypotheses",
            "30 bowls before 9 a.m.; working hypothesis 30 to 60 in the window; Stage 1 table 20 to 35 bowls per day.",
            "No. Optional scenario cell is blank. Example tab uses some of these volumes as illustrations.",
            "docs/oats-and-more/README.md; decision-log.md; pilot-and-equipment.md; validation-backlog.md; Challenger round 2 (the 30 to 60 figure has no headcount source)",
        ),
        (
            "Archive average ticket of $7.50",
            "Model input in the Stage 1 gross-sales table. Not a measured mix. A $5.95 Classic-only mix would lower gross.",
            "No, not used as the model default. Used on the example tab and as a sensitivity stress case.",
            "docs/oats-and-more/research/pilot-and-equipment.md; notes/oe-challenger/adversarial-review-round-2-2026-11-11.md, objection 3",
        ),
        (
            "Weeks per month 4.33",
            "Converter used in the archive's monthly gross-sales math.",
            "Yes, editable on 01_Operations_and_menu.",
            "docs/oats-and-more/research/pilot-and-equipment.md",
        ),
        (
            "Selling channels",
            "Employer-paid catering, employee preorder and pickup, indoor office counter, or a possible residency. Hosted private commercial location with approved plug-in power is the current site hypothesis.",
            "No numbers. Qualitative context only.",
            "docs/oats-and-more/research/boise-kitchen-and-office-service-market-2026-11-11.md; docs/oats-and-more/README.md",
        ),
        (
            "Advertised kitchen rates",
            "Gina's $40/hr; Flava $30/hr (4-hour session may apply); Commons $40/$20; Osage $35/$25 with a two-hour minimum and a noted onboarding fee. Advertised, not reserved.",
            "No. Notes only. The example tab uses $30 and $40 with 2 hours, as in that memo's illustrative check.",
            "docs/oats-and-more/research/boise-kitchen-and-office-service-market-2026-11-11.md",
        ),
        (
            "Published health-department example fees",
            "Plan review $100; example mobile license $80 or $100 depending on category. Confirm at application. A portable stand may be classified differently.",
            "No. Notes only. Do not paste into the model until confirmed.",
            "docs/oats-and-more/research/local-regulation.md",
        ),
        (
            "Flavor poll",
            "Directional interest among website visitors. Not paid demand at a price, time, and place.",
            "No volume is taken from the poll.",
            "integrations/oats-voting/README.md; validation-backlog.md; notes/oe-challenger/adversarial-review-2026-11-11.md",
        ),
        (
            "Weeks per year 52",
            "Used only to convert a per-year cost into a weekly amount.",
            "Yes, inside the weekly-cost formula on 04_Fixed_costs (divisor 52).",
            "Modeling convention, stated here. Close to 4.33 times 12 (51.96).",
        ),
    ]
    for i, (topic, assumed, prefill, src) in enumerate(sources):
        r = 6 + i
        paint(ws.cell(r, 1, topic), font=font_label, fill=fill_gray, align=wrap_left)
        paint(ws.cell(r, 2, assumed), font=font_label, fill=fill_cream, align=wrap_left)
        paint(ws.cell(r, 3, prefill), font=font_label, fill=fill_cream, align=wrap_left)
        paint(ws.cell(r, 4, src), font=font_small, fill=fill_cream, align=wrap_left)
        ws.row_dimensions[r].height = 48

    r0 = 6 + len(sources) + 1
    header_bar(ws, r0, "D", "Formulas, written out")
    formulas = [
        "Cost of one ingredient or packaging piece per bowl = purchase price divided by purchase quantity, times the amount used in one bowl. Use the same unit for both quantities.",
        "Bowl ingredient cost = shared oatmeal base cost + toppings for that bowl.",
        "Weighted ingredient cost = sum of (bowl ingredient cost times that bowl's share of sales). Shares must add to 100% or to 1.00.",
        "Payment fee per bowl = (average ticket times card-fee percent + per-transaction fee) times the share paid by card. Blank card fields are treated as $0 and listed as omitted.",
        "Spoilage per bowl = ingredient cost times spoilage percent. Blank is treated as $0 and listed as omitted.",
        "Variable cost per bowl (V) = ingredient cost + packaging + payment fee + spoilage + other per-bowl cost + host percent of ticket.",
        "Contribution per bowl (C) = average ticket (T) minus V.",
        "Kitchen cost per selling day = hourly rate times the larger of reserved hours and any numeric minimum booking.",
        "Weekly fixed cost (F) = (per-day costs times selling days) + per-week costs + (per-month costs divided by weeks per month) + (per-year costs divided by 52). Startup recovery is added only if you enter a recovery period in months.",
        "Break-even bowls per week = F divided by C, only if C is greater than 0 and required inputs are filled. Otherwise the workbook says fill me in, or that the ticket must be higher than variable cost.",
        "Break-even bowls per selling day = weekly break-even divided by selling days per week.",
        "Weekly profit at a scenario volume = C times bowls per week, minus F. No operator wage is subtracted.",
        "Profit per hour = weekly profit divided by weekly hours.",
        "Monthly figures = weekly figures times weeks per month (default assumption 4.33).",
        "Secondary income-target scenario: bowls per week to leave a target cash amount I = (F + I) divided by C. That view is not the Stage 1 goal.",
    ]
    for i, text in enumerate(formulas):
        r = r0 + 1 + i
        merge(ws, f"A{r}:D{r}", f"{i+1}. {text}", font=font_label, fill=fill_cream, height=32)

    last = r0 + 1 + len(formulas) + 1
    header_bar(ws, last, "D", "What was deliberately not used")
    merge(
        ws,
        f"A{last+1}:D{last+3}",
        (
            "No invented typical food-cost percentage. No invented payment-processor rate. "
            "No competitor prices or market-size figures from outside the repository. "
            "No poll tallies as sales volume. No new kitchen or permit research beyond what is already in the archive. "
            "Confirming a kitchen and a license path is other work. "
            "Files under notes/oe-challenger/ and the builder's site files were not modified."
        ),
        font=font_label,
        fill=fill_cream,
    )
    for r in range(last + 1, last + 4):
        ws.row_dimensions[r].height = 20

    ws.freeze_panes = "A5"
    return ws


def main():
    here = Path(__file__).resolve().parent
    out = here / OUT_NAME
    wb = Workbook()
    wb.properties.title = "Oats, Etc. Stage 1 cost and break-even model"
    wb.properties.creator = "OE Numbers"
    wb.properties.description = (
        "Blank cost template and break-even model for the Oats, Etc. Stage 1 breakfast pilot. "
        "A break-even experiment to learn from, not a living-wage plan. No macros."
    )
    build_start(wb)
    build_operations(wb)
    build_ingredients(wb)
    build_packaging(wb)
    build_fixed(wb)
    build_hours(wb)
    build_breakeven(wb)
    build_income(wb)
    build_sensitivity(wb)
    build_example(wb)
    build_sources(wb)
    wb.save(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
