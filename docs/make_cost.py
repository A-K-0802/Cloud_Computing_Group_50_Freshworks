import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ensure results directories exist
os.makedirs("results", exist_ok=True)
os.makedirs("serverless-coldstart/results", exist_ok=True)

wb = Workbook()
ws = wb.active
ws.title = "Cost Analysis"

rows = [
    ("Input", "Value", "Note"),
    ("Billed duration (ms)", 33.39, "B's CloudWatch measured average"),
    ("Memory (GB)", 0.125, "128 MB configured in template.yaml"),
    ("API Gateway $/million", 1.00, "HTTP API rate in ap-south-1"),
    ("Lambda requests $/million", 0.20, "Lambda invocation rate"),
    ("Lambda $/GB-second", 0.0000166667, "Lambda compute tier rate"),
    ("DynamoDB $/million writes", 1.25, "On-Demand write rate ap-south-1"),
    ("EC2 t3.micro $/hour", 0.0104, "Always-on comparison (ap-south-1)"),
    ("", "", ""),
    ("Cost per 1,000 requests", "", ""),
    ("API Gateway", "=B4/1000", "$0.00100"),
    ("Lambda requests", "=B5/1000", "$0.00020"),
    ("Lambda compute", "=B3*(B2/1000)*B6*1000", "$0.00007"),
    ("DynamoDB write", "=B7/1000", "$0.00125"),
    ("TOTAL per 1,000", "=SUM(B11:B14)", "$0.00252 per 1,000 requests"),
    ("", "", ""),
    ("EC2 monthly (24/7)", "=B8*730", "$7.59 per month"),
    ("Break-even requests/month", "=B17/(B15/1000)", "~3,010,000 requests/month"),
]

for r in rows:
    ws.append(r)

# Styling and formatting
header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
section_font = Font(name="Calibri", size=11, bold=True, color="1F497D")
highlight_fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
bold_font = Font(name="Calibri", size=11, bold=True)
regular_font = Font(name="Calibri", size=11)
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

for col in range(1, 4):
    cell = ws.cell(row=1, column=col)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center" if col == 2 else "left")

for row_idx, r in enumerate(rows[1:], start=2):
    title = r[0]
    val = r[1]
    cell_a = ws.cell(row=row_idx, column=1)
    cell_b = ws.cell(row=row_idx, column=2)
    cell_c = ws.cell(row=row_idx, column=3)

    if title in ("Cost per 1,000 requests",):
        cell_a.font = section_font
    elif title in ("TOTAL per 1,000", "Break-even requests/month"):
        cell_a.font = bold_font
        cell_b.font = bold_font
        cell_c.font = bold_font
        cell_a.fill = highlight_fill
        cell_b.fill = highlight_fill
        cell_c.fill = highlight_fill
    elif title == "EC2 monthly (24/7)":
        cell_a.font = bold_font
        cell_b.font = bold_font
    elif title != "":
        cell_a.font = regular_font
        cell_b.font = regular_font
        cell_c.font = regular_font

    if title != "":
        for cell in (cell_a, cell_b, cell_c):
            cell.border = thin_border

# Auto-fit column widths
ws.column_dimensions['A'].width = 30
ws.column_dimensions['B'].width = 24
ws.column_dimensions['C'].width = 38

# Save in both results locations
wb.save("results/cost.xlsx")
wb.save("serverless-coldstart/results/cost.xlsx")
print("results/cost.xlsx and serverless-coldstart/results/cost.xlsx generated successfully!")
