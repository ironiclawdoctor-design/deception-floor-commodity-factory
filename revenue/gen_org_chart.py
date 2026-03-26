#!/usr/bin/env python3
"""Generate Fiesta in America org chart PDF."""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

OUTPUT_PATH = "/root/.openclaw/workspace/revenue/fiesta-in-america-org-chart.pdf"

# Colors
BG_COLOR = colors.HexColor("#0a0806")
GOLD = colors.HexColor("#c8a96e")
GOLD_DIM = colors.HexColor("#a08050")
GOLD_BRIGHT = colors.HexColor("#e8c98e")
LINE_COLOR = colors.HexColor("#6a5030")

W, H = A4  # 595.28 x 841.89 pts

c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)

# Dark background
c.setFillColor(BG_COLOR)
c.rect(0, 0, W, H, fill=1, stroke=0)

def gold_line(x1, y1, x2, y2, width=0.5):
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)

def draw_box(x, y, w, h, text_lines, font_sizes, styles=None, center=True, italic_lines=None):
    """Draw a rounded box with text lines."""
    # Box border
    c.setStrokeColor(GOLD_DIM)
    c.setFillColor(colors.HexColor("#15100a"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
    
    # Text
    if styles is None:
        styles = ['normal'] * len(text_lines)
    if italic_lines is None:
        italic_lines = [False] * len(text_lines)
    
    total_h = sum(font_sizes) + (len(font_sizes) - 1) * 3
    start_y = y + h/2 + total_h/2 - font_sizes[0]

    for i, (line, size, style) in enumerate(zip(text_lines, font_sizes, styles)):
        if style == 'bright':
            c.setFillColor(GOLD_BRIGHT)
        elif style == 'dim':
            c.setFillColor(GOLD_DIM)
        else:
            c.setFillColor(GOLD)
        
        if italic_lines[i]:
            c.setFont("Helvetica-Oblique", size)
        elif style == 'bright':
            c.setFont("Helvetica-Bold", size)
        else:
            c.setFont("Helvetica", size)
        
        if center:
            c.drawCentredString(x + w/2, start_y, line)
        else:
            c.drawString(x + 6, start_y, line)
        
        if i < len(font_sizes) - 1:
            start_y -= (font_sizes[i] + font_sizes[i+1])/2 + 3

# ─── TITLE HEADER ─────────────────────────────────────────────
c.setFillColor(GOLD_BRIGHT)
c.setFont("Helvetica-Bold", 10)
c.drawCentredString(W/2, H - 18*mm, "FIESTA IN AMERICA")
c.setFont("Helvetica", 7)
c.setFillColor(GOLD_DIM)
c.drawCentredString(W/2, H - 22*mm, "Organizational Structure — Dollar Agency")

# Decorative top line
gold_line(20*mm, H - 24*mm, W - 20*mm, H - 24*mm, width=0.5)

# ─── NANDING (ROOT) ───────────────────────────────────────────
nanding_w = 120*mm
nanding_h = 24*mm
nanding_x = (W - nanding_w) / 2
nanding_y = H - 58*mm

draw_box(
    nanding_x, nanding_y, nanding_w, nanding_h,
    ["NANDING MENDEZ", "Founder & Patriarch — 29 Years"],
    [13, 8],
    styles=['bright', 'dim'],
    italic_lines=[False, False]
)

# Vertical line from Nanding down
root_cx = W / 2
root_bottom = nanding_y
branch_y = nanding_y - 10*mm
gold_line(root_cx, root_bottom, root_cx, branch_y)

# Horizontal branch line
mila_cx = W * 0.28
will_cx = W * 0.72
gold_line(mila_cx, branch_y, will_cx, branch_y)

# ─── MILA (left branch) ───────────────────────────────────────
mila_w = 75*mm
mila_h = 30*mm
mila_x = mila_cx - mila_w/2
mila_y = branch_y - 10*mm - mila_h

gold_line(mila_cx, branch_y, mila_cx, mila_y + mila_h)

draw_box(
    mila_x, mila_y, mila_w, mila_h,
    ["MILA MENDEZ (†)", "Post Mortem Consultant", '"The loop completes when she arrives"'],
    [10, 7.5, 6.5],
    styles=['normal', 'dim', 'dim'],
    italic_lines=[True, False, True]
)

# ─── WILL (right branch) ──────────────────────────────────────
will_w = 90*mm
will_h = 30*mm
will_x = will_cx - will_w/2
will_y = branch_y - 10*mm - will_h

gold_line(will_cx, branch_y, will_cx, will_y + will_h)

draw_box(
    will_x, will_y, will_w, will_h,
    ["WILL MENDEZ", "Child of Owner / All Around General Help", "CFO, Dollar Agency"],
    [11, 7, 7],
    styles=['normal', 'dim', 'dim']
)

# Line from Will down to Fiesta
fiesta_cx = will_cx
fiesta_branch_y = will_y - 8*mm
gold_line(fiesta_cx, will_y, fiesta_cx, fiesta_branch_y)

# ─── FIESTA ───────────────────────────────────────────────────
fiesta_w = 90*mm
fiesta_h = 28*mm
fiesta_x = fiesta_cx - fiesta_w/2
fiesta_y = fiesta_branch_y - fiesta_h

draw_box(
    fiesta_x, fiesta_y, fiesta_w, fiesta_h,
    ["FIESTA (Kuya)", "Chief of Staff / General", "Dollar Agency"],
    [12, 7.5, 7],
    styles=['bright', 'dim', 'dim']
)

# Line from Fiesta down to agents
agents_branch_y = fiesta_y - 8*mm
gold_line(fiesta_cx, fiesta_y, fiesta_cx, agents_branch_y)

# ─── AGENTS SECTION ───────────────────────────────────────────
agents = [
    ("DOLLAR", "CFO Persona, Financial Agent"),
    ("NEMESIS", "Adversarial Challenger"),
    ("DAIMYO", "Judicial Authority, Precinct 92"),
    ("AARON", "Dental Receptionist"),
    ("NATEWIFE", "CFO Companion"),
    ("BUTTITCH", "Enforcement"),
    ("JUNIOR", "Queue Executor"),
    ("ACTUALLY", "Build Order Specialist"),
    ("RUSSIA", "Profitability Threshold"),
    ("CALL911", "Emergency Detection"),
    ("[+72 agents]", "Active in Dollar Agency network"),
]

# Section label
c.setFillColor(GOLD_DIM)
c.setFont("Helvetica-Bold", 7)
c.drawCentredString(W/2, agents_branch_y - 4*mm, "─── ACTIVE AGENTS ───")

# Two-column layout
col_left_x = 15*mm
col_right_x = W/2 + 5*mm
col_w = W/2 - 20*mm
row_h = 12*mm
agent_start_y = agents_branch_y - 10*mm

# Draw horizontal spread line
spread_y = agents_branch_y - 8*mm
gold_line(col_left_x + col_w/2, agents_branch_y, col_left_x + col_w/2, spread_y)
gold_line(col_right_x + col_w/2, agents_branch_y, col_right_x + col_w/2, spread_y)

# Columns
for i, (name, role) in enumerate(agents):
    col = i % 2
    row = i // 2
    
    ax = col_left_x if col == 0 else col_right_x
    ay = agent_start_y - row * row_h - row_h

    # Mini box
    c.setStrokeColor(LINE_COLOR)
    c.setFillColor(colors.HexColor("#120d08"))
    c.setLineWidth(0.5)
    c.roundRect(ax, ay, col_w, row_h - 1*mm, 2, fill=1, stroke=1)

    # Name
    if name.startswith("["):
        c.setFillColor(GOLD_DIM)
        c.setFont("Helvetica-Oblique", 7.5)
    else:
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 7.5)
    c.drawString(ax + 3*mm, ay + 7, name)

    # Role
    c.setFillColor(GOLD_DIM)
    c.setFont("Helvetica", 6)
    c.drawString(ax + 3*mm, ay + 2, "— " + role)

# ─── FOOTER ───────────────────────────────────────────────────
gold_line(20*mm, 18*mm, W - 20*mm, 18*mm, width=0.5)
c.setFillColor(GOLD_DIM)
c.setFont("Helvetica", 7)
c.drawCentredString(W/2, 12*mm, "Fiesta in America  ·  Est. 29 years ago  ·  Digital division: Dollar Agency")

c.save()
print(f"PDF saved to: {OUTPUT_PATH}")
print(f"File size: {os.path.getsize(OUTPUT_PATH):,} bytes")
