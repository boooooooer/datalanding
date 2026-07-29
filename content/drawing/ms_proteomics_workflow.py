"""Mass Spectrometry Proteomics Full Pipeline Workflow.
Cell → Protein Extraction → Drug/Control split → Digestion → LC-MS → Data → Output
"""
import drawsvg as draw
import math

W, H = 1200, 700
d = draw.Drawing(W, H, origin=(0, 0), displayInline=False)

# Colors
BG = '#F7F4EF'
PRI = '#7B9BA6'   # Morandi blue
SEC = '#8AA79C'   # Morandi sage
ACC = '#B8956A'   # Morandi warm
DARK = '#2C3E50'
WHITE = '#FFFFFF'
LIGHT = '#E8E3DB'
DRUG_C = '#C47A6B'
CTRL_C = '#6B8F9B'
GRAY = 'rgba(44,62,80,0.5)'

# Background
d.append(draw.Rectangle(0, 0, W, H, fill=BG))

# ===== HELPERS =====
def draw_box(x, y, w, h, fill=WHITE, rx=8):
    d.append(draw.Rectangle(x-w/2+2, y-2, w, h, fill='rgba(0,0,0,0.05)', rx=rx))
    d.append(draw.Rectangle(x-w/2, y, w, h, fill=fill, rx=rx))

def draw_text(x, y, text, size=12, color=DARK, bold=False, anchor='middle'):
    d.append(draw.Text(text, size, x, y, fill=color, font_family='sans-serif',
              font_weight='bold' if bold else 'normal', text_anchor=anchor))

def draw_arrow(x1, y1, x2, y2, color=PRI, w=2.5):
    p = draw.Path(stroke=color, stroke_width=w, fill='none')
    p.M(x1, y1); p.L(x2, y2)
    d.append(p)
    angle = math.atan2(y2-y1, x2-x1)
    ah = 9
    p2 = draw.Path(fill=color)
    p2.M(x2, y2)
    p2.L(x2-ah*math.cos(angle-0.45), y2-ah*math.sin(angle-0.45))
    p2.L(x2-ah*math.cos(angle+0.45), y2-ah*math.sin(angle+0.45))
    p2.Z()
    d.append(p2)

def draw_circle(cx, cy, r, fill, opacity=0.7):
    d.append(draw.Circle(cx, cy, r, fill=fill, fill_opacity=opacity))

# ===== TITLE =====
draw_text(W/2, 30, 'Mass Spectrometry-Based Proteomics Pipeline', 22, DARK, bold=True)
draw_text(W/2, 52, 'Bottom-up Proteomics: From Cell Culture to Differential Abundance', 13, GRAY)

# ===== LAYOUT: 7 stages in a flow with split in the middle =====
# Stage 1: Cells (x~100)
# Stage 2: Protein Extraction (x~260)
# Stage 3: Drug Treatment (x~430, y~upper) + Blank Control (x~430, y~lower)
# Stage 4: Merge → Digestion (x~600)
# Stage 5: LC Separation (x~740, y~upper)
# Stage 6: MS Analysis (x~740, y~lower)
# Stage 7: Data Analysis + Output (x~900, x~1050)

BASE_Y = 380
HIGH_Y = 500
LOW_Y = 260

# ---- STAGE 1: CELL CULTURE (x=80) ----
cx, cy = 80, BASE_Y
# Cell cluster
for dx, dy, r, c in [(-8,5,18,PRI), (15,-2,14,SEC), (18,12,12,ACC), (-15,-10,10,PRI)]:
    draw_circle(cx+dx, cy+dy, r, c)
draw_text(cx, cy-50, 'Cell Culture', 13, DARK, bold=True)
draw_text(cx, cy-68, 'Cell Line / Tissue', 10, GRAY)

draw_arrow(cx+50, cy, 140, cy)

# ---- STAGE 2: PROTEIN EXTRACTION (x=190) ----
cx = 190
draw_box(cx, cy-30, 140, 80, WHITE)
draw_text(cx, cy+5, 'Protein Extraction', 12, PRI, bold=True)
draw_text(cx, cy-20, 'Lysis / Denaturation', 9, GRAY)
draw_text(cx, cy-38, 'Reduction / Alkylation', 9, GRAY)
draw_text(cx, cy-56, 'Precipitation / Cleanup', 9, GRAY)

# ---- SPLIT ----
draw_arrow(cx+70, cy, 295, HIGH_Y, color=DRUG_C)
draw_arrow(cx+70, cy, 295, LOW_Y, color=CTRL_C)

# ---- STAGE 3a: DRUG TREATMENT (x=380, y=HIGH_Y) ----
cy_d = HIGH_Y
draw_box(380, cy_d-35, 170, 85, '#F5EEEC')
draw_text(380, cy_d+2, 'Drug Treatment', 13, DRUG_C, bold=True)
draw_text(380, cy_d-20, 'Ligand / Inhibitor Incubation', 9, GRAY)
draw_text(380, cy_d-40, 'Target Binding / Conformational Change', 9, GRAY)
draw_text(380, cy_d-58, 'n = 3 biological replicates', 9, GRAY)

# ---- STAGE 3b: BLANK CONTROL (x=380, y=LOW_Y) ----
cy_c = LOW_Y
draw_box(380, cy_c-35, 170, 85, '#ECF0F2')
draw_text(380, cy_c+2, 'Vehicle Control', 13, CTRL_C, bold=True)
draw_text(380, cy_c-20, 'DMSO / Buffer Only', 9, GRAY)
draw_text(380, cy_c-40, 'No Target Engagement', 9, GRAY)
draw_text(380, cy_c-58, 'n = 3 biological replicates', 9, GRAY)

# ---- MERGE ----
draw_arrow(380+85, cy_d, 530, BASE_Y+20, color=DRUG_C)
draw_arrow(380+85, cy_c, 530, BASE_Y-20, color=CTRL_C)

# Merge node
draw_circle(550, BASE_Y, 16, ACC, 0.9)
draw_text(550, BASE_Y+2, 'Merge', 10, WHITE, bold=True)
draw_text(550, BASE_Y-25, 'Parallel Processing', 8, GRAY)

draw_arrow(566, BASE_Y, 620, BASE_Y)

# ---- STAGE 4: DIGESTION (x=660) ----
draw_box(660, BASE_Y-35, 140, 95, WHITE)
draw_text(660, BASE_Y+8, 'Trypsin Digestion', 12, PRI, bold=True)
draw_text(660, BASE_Y-15, 'Enzymatic Cleavage', 9, GRAY)
draw_text(660, BASE_Y-33, 'Peptide Mixture', 9, GRAY)
draw_text(660, BASE_Y-51, '~100K peptides/sample', 9, GRAY)
draw_text(660, BASE_Y-69, 'C18 Desalting / Cleanup', 9, GRAY)

draw_arrow(660+70, BASE_Y, 760, BASE_Y)

# ---- STAGE 5: LC SEPARATION (x=810, upper) ----
cx_lc = 810
draw_box(cx_lc, HIGH_Y-25, 130, 70, LIGHT)
draw_text(cx_lc, HIGH_Y+5, 'LC Separation', 11, PRI, bold=True)
draw_text(cx_lc, HIGH_Y-15, 'RP-HPLC Gradient', 9, GRAY)
draw_text(cx_lc, HIGH_Y-35, 'Peptide Fractionation', 9, GRAY)

draw_arrow(cx_lc, HIGH_Y-60, cx_lc, BASE_Y+50, color=SEC)

# ---- STAGE 6: MS ANALYSIS (x=810, lower) ----
cx_ms = 810
draw_box(cx_ms, BASE_Y-40, 160, 90, WHITE)
draw_text(cx_ms, BASE_Y, 'LC-MS/MS Analysis', 12, PRI, bold=True)
draw_text(cx_ms, BASE_Y-22, 'ESI Ionization', 9, GRAY)
draw_text(cx_ms, BASE_Y-40, 'Orbitrap MS1 Full Scan', 9, GRAY)
draw_text(cx_ms, BASE_Y-58, 'HCD/CID Fragmentation', 9, GRAY)
draw_text(cx_ms, BASE_Y-76, 'MS2 Spectra Acquisition', 9, GRAY)

# Mini spectrum visualization
for i in range(12):
    h_vals = [15,35,8,22,42,12,28,6,32,18,40,10]
    d.append(draw.Rectangle(cx_ms-70+i*11, BASE_Y-120, 8, h_vals[i],
             fill=PRI, fill_opacity=0.5))

draw_arrow(cx_ms+80, BASE_Y, 930, BASE_Y)

# ---- STAGE 7: DATA ANALYSIS (x=980) ----
draw_box(980, BASE_Y-30, 175, 100, WHITE)
draw_text(980, BASE_Y+15, 'Data Analysis', 13, PRI, bold=True)
draw_text(980, BASE_Y-8, 'Database Search', 9, GRAY)
draw_text(980, BASE_Y-26, 'Protein ID (FDR < 1%)', 9, GRAY)
draw_text(980, BASE_Y-44, 'Label-Free Quantification', 9, GRAY)
draw_text(980, BASE_Y-62, 'Drug vs Control Comparison', 9, GRAY)
draw_text(980, BASE_Y-80, 'Statistical Testing / Filtering', 9, GRAY)

draw_arrow(980+88, BASE_Y, 1110, BASE_Y)

# ---- STAGE 8: OUTPUT (x=1130) ----
draw_box(1130, BASE_Y-40, 110, 105, ACC)
draw_text(1130, BASE_Y+8, 'Differential', 12, WHITE, bold=True)
draw_text(1130, BASE_Y-8, 'Abundance', 12, WHITE, bold=True)
draw_text(1130, BASE_Y-28, 'Volcano Plot', 9, 'rgba(255,255,255,0.75)')
draw_text(1130, BASE_Y-44, 'Heatmap', 9, 'rgba(255,255,255,0.75)')
draw_text(1130, BASE_Y-60, 'Pathway Enrichment', 9, 'rgba(255,255,255,0.75)')
draw_text(1130, BASE_Y-76, 'Candidate Targets', 9, 'rgba(255,255,255,0.75)')

# ===== SECTION LABELS =====
draw_text(80, 620, 'Sample Prep', 11, PRI, bold=True)
draw_text(380, 620, 'Perturbation', 11, PRI, bold=True)
draw_text(660, 620, 'Proteolysis', 11, PRI, bold=True)
draw_text(810, 620, 'Acquisition', 11, PRI, bold=True)
draw_text(980, 620, 'Bioinformatics', 11, PRI, bold=True)
draw_text(1130, 620, 'Results', 11, PRI, bold=True)

# Section divider line
d.append(draw.Line(30, 610, W-30, 610, stroke='rgba(123,155,166,0.3)', stroke_width=1))

# ===== SAVE =====
d.save_svg('ms_proteomics_workflow.svg')
print('Saved: ms_proteomics_workflow.svg')
print(f'Size: {W}x{H}')
