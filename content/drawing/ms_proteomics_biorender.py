"""Mass Spectrometry Proteomics — BioRender-Quality Workflow with Real Bioicons."""
import drawsvg as draw
import math, base64, os

W, H = 1400, 900
d = draw.Drawing(W, H, origin=(0, 0), displayInline=False)

# Colors
BG = '#F7F4EF'
PRI = '#7B9BA6'
SEC = '#8AA79C'
ACC = '#B8956A'
DARK = '#2C3E50'
WHITE = '#FFFFFF'
GRAY = 'rgba(44,62,80,0.5)'
DRUG_C = '#C47A6B'
CTRL_C = '#6B8F9B'
MUTED_RED = '#D4958A'

# Background
d.append(draw.Rectangle(0, 0, W, H, fill=BG))

def load_svg_b64(path):
    """Load SVG file as base64 data URI."""
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return f'data:image/svg+xml;base64,{data}'

def icon(x, y, w, h, path):
    """Place an icon at center (x,y) with given dimensions."""
    uri = load_svg_b64(path)
    d.append(draw.Image(x-w/2, y-h/2, w, h, data=uri.encode(), mimeType='image/svg+xml'))

def box(x, y, w, h, fill=WHITE, rx=10, alpha=1.0):
    d.append(draw.Rectangle(x-w/2+2, y+2, w, h, fill='rgba(0,0,0,0.05)', rx=rx))
    d.append(draw.Rectangle(x-w/2, y, w, h, fill=fill, fill_opacity=alpha, rx=rx))

def txt(x, y, text, size=12, color=DARK, bold=False, anchor='middle'):
    d.append(draw.Text(text, size, x, y, fill=color, font_family='sans-serif',
              font_weight='bold' if bold else 'normal', text_anchor=anchor))

def arrow(x1, y1, x2, y2, color=PRI, w=3):
    p = draw.Path(stroke=color, stroke_width=w, fill='none')
    p.M(x1, y1); p.L(x2, y2)
    d.append(p)
    angle = math.atan2(y2-y1, x2-x1)
    ah = 10
    p2 = draw.Path(fill=color)
    p2.M(x2, y2)
    p2.L(x2-ah*math.cos(angle-0.45), y2-ah*math.sin(angle-0.45))
    p2.L(x2-ah*math.cos(angle+0.45), y2-ah*math.sin(angle+0.45))
    p2.Z()
    d.append(p2)

# ===== SECTION DIVIDERS =====
# Top bar
d.append(draw.Rectangle(0, 0, W, 55, fill=PRI, fill_opacity=0.08))
txt(W/2, 20, 'Mass Spectrometry-Based Proteomics: Full Experimental Pipeline', 22, DARK, bold=True)
txt(W/2, 42, 'Drug Treatment vs Vehicle Control - Bottom-Up Quantitative Proteomics Workflow', 12, GRAY)

# ===== ROW 1: BIOLOGICAL SAMPLE & TREATMENT (y=80-320) =====
Y1 = 80

# ---- CELL CULTURE SOURCE (left) ----
box(100, Y1+120, 150, 220, WHITE)
txt(100, Y1+215, 'Mammalian', 11, DARK, bold=True)
txt(100, Y1+200, 'Cell Culture', 11, DARK, bold=True)
icon(100, Y1+105, 120, 100, 'bioicons/cell_culture.svg')

arrow(175, Y1+120, 250, Y1+120)

# ---- SPLIT ----
txt(250, Y1+80, 'Parallel', 10, GRAY)
txt(250, Y1+65, 'TMT Labeling', 10, PRI, bold=True)

arrow(270, Y1+120, 310, Y1+200, color=DRUG_C)
arrow(270, Y1+120, 310, Y1+40, color=CTRL_C)

# ---- DRUG TREATMENT (top right) ----
Y_DRUG = Y1+200
box(460, Y_DRUG+70, 200, 160, '#F8F0EE')
txt(460, Y_DRUG+135, 'Drug Treatment Group', 13, DRUG_C, bold=True)
txt(460, Y_DRUG+115, 'Ligand / Inhibitor', 10, GRAY)
icon(460, Y_DRUG+30, 90, 80, 'bioicons/receptor.svg')
txt(460, Y_DRUG-25, 'Drug binds to target', 10, DRUG_C)
txt(460, Y_DRUG-40, 'Conformational change', 10, GRAY)

# ---- VEHICLE CONTROL (bottom right) ----
Y_CTRL = Y1+40
box(460, Y_CTRL+70, 200, 160, '#ECF0F2')
txt(460, Y_CTRL+135, 'Vehicle Control Group', 13, CTRL_C, bold=True)
txt(460, Y_CTRL+115, 'DMSO / Buffer Only', 10, GRAY)
icon(460, Y_CTRL+30, 90, 80, 'bioicons/test_tube.svg')
txt(460, Y_CTRL-25, 'No target engagement', 10, CTRL_C)
txt(460, Y_CTRL-40, 'Baseline reference', 10, GRAY)

# Arrows from both → merge
arrow(560, Y_DRUG+70, 620, Y1+120, color=DRUG_C)
arrow(560, Y_CTRL+70, 620, Y1+120, color=CTRL_C)

# ===== ROW 2: PROTEIN EXTRACTION (y=350-520) =====
Y2 = 380

box(710, Y2+65, 160, 150, WHITE)
txt(710, Y2+125, 'Protein Extraction', 13, PRI, bold=True)
txt(710, Y2+105, 'Cell Lysis / Reduction', 9, GRAY)
txt(710, Y2+90, 'Alkylation / Cleanup', 9, GRAY)
icon(710, Y2+10, 100, 80, 'bioicons/centrifuge.svg')

arrow(790, Y2+65, 870, Y2+65)

# ===== ROW 3: DIGESTION (x=920) =====
box(920, Y2+65, 150, 150, WHITE)
txt(920, Y2+125, 'Trypsin Digestion', 13, PRI, bold=True)
txt(920, Y2+105, 'Enzymatic Cleavage', 9, GRAY)
txt(920, Y2+90, 'Peptide Mixture', 9, GRAY)
txt(920, Y2+75, 'C18 Desalting', 9, GRAY)
icon(920, Y2+5, 100, 60, 'bioicons/enzyme.svg')

# Peptide output visual
for i in range(5):
    w_p = 12 + (i%2)*4
    d.append(draw.Rectangle(880+i*18, Y2+65-90, w_p, 20, fill=PRI, fill_opacity=0.5, rx=3))
txt(920, Y2+65-110, '~100K peptides', 9, GRAY)

arrow(995, Y2+65, 1060, Y2+65)

# ===== ROW 4: LC-MS/MS (x=1110) =====
box(1120, Y2+65, 160, 180, WHITE)
txt(1120, Y2+140, 'LC-MS/MS Analysis', 13, PRI, bold=True)
txt(1120, Y2+120, 'RP-HPLC Gradient', 9, GRAY)
txt(1120, Y2+105, 'ESI Ionization', 9, GRAY)
txt(1120, Y2+90, 'Orbitrap MS1 Scan', 9, GRAY)
txt(1120, Y2+75, 'HCD Fragmentation', 9, GRAY)
txt(1120, Y2+60, 'MS2 Spectra', 9, GRAY)
icon(1120, Y2-20, 130, 70, 'bioicons/lc_ms.svg')

# Mini mass spectrum
spec_cy = Y2+65-100
for i in range(15):
    hs = [22,45,10,28,58,15,35,8,42,18,52,12,30,48,20]
    d.append(draw.Rectangle(1070+i*14, spec_cy, 9, hs[i], fill=PRI, fill_opacity=0.55, rx=2))
txt(1120, spec_cy-20, 'MS Spectrum', 9, GRAY)

arrow(1200, Y2+65, 1260, Y2+65)

# ===== ROW 5: DATA ANALYSIS =====
box(1310, Y2+65, 140, 160, WHITE)
txt(1310, Y2+130, 'Data Analysis', 13, PRI, bold=True)
txt(1310, Y2+110, 'MaxQuant / DIA-NN', 9, GRAY)
txt(1310, Y2+95, 'Database Search', 9, GRAY)
txt(1310, Y2+80, 'Protein ID FDR<1%', 9, GRAY)
txt(1310, Y2+65, 'LFQ Normalization', 9, GRAY)
txt(1310, Y2+50, 'Statistical Testing', 9, GRAY)
icon(1310, Y2-15, 100, 70, 'bioicons/microscope.svg')

arrow(1380, Y2+65, 1380, Y2+65+140)

# ===== ROW 6: FINAL OUTPUT =====
Y3 = Y2+220
box(1310, Y3+65, 140, 150, ACC)
txt(1310, Y3+125, 'Differential', 12, WHITE, bold=True)
txt(1310, Y3+110, 'Abundance', 12, WHITE, bold=True)
txt(1310, Y3+90, 'Volcano Plot', 9, 'rgba(255,255,255,0.75)')
txt(1310, Y3+75, 'Heatmap Clustering', 9, 'rgba(255,255,255,0.75)')
txt(1310, Y3+60, 'Pathway Analysis', 9, 'rgba(255,255,255,0.75)')
txt(1310, Y3+45, 'Candidate Targets', 9, 'rgba(255,255,255,0.75)')

# Volcano mini
for i in range(18):
    vx = 1240 + i*7
    vy = Y3 + [-15,-10,20,30,25,-5,-18,35,15,10,-22,40,-8,28,5,22,-12,18][i]
    vc = ACC if abs(vy-Y3) > 18 else (DRUG_C if vy > Y3 else CTRL_C)
    d.append(draw.Circle(vx, vy, [2.5, 3.5, 4, 5, 3, 2, 2.5, 6, 3.5, 2.5, 3, 7, 2, 4, 2.5, 3.5, 2, 5][i],
             fill=vc, fill_opacity=0.8))

# ===== BOTTOM: ANNOTATIONS =====
Y_BOT = 760
d.append(draw.Rectangle(40, Y_BOT, W-80, 110, fill='rgba(123,155,166,0.06)', rx=12))

# Step indicators
steps = [
    (100,  'Cell Culture\n& Treatment',  PRI),
    (460,  'Protein\nExtraction',        PRI),
    (920,  'Enzymatic\nDigestion',       PRI),
    (1120, 'LC-MS/MS\nAcquisition',      PRI),
    (1310, 'Data Analysis\n& Results',   PRI),
]
for sx, slabel, scolor in steps:
    txt(sx, Y_BOT+80, slabel, 10, scolor, bold=True)

# Legend
txt(700, Y_BOT+80, 'Pipeline Legend:', 10, DARK, bold=True)
d.append(draw.Rectangle(700, Y_BOT+55, 14, 14, fill=DRUG_C, rx=3))
txt(780, Y_BOT+62, 'Drug Treatment Path', 9, GRAY)
d.append(draw.Rectangle(700, Y_BOT+35, 14, 14, fill=CTRL_C, rx=3))
txt(780, Y_BOT+42, 'Control Path', 9, GRAY)
txt(700, Y_BOT+20, 'Icons: Bioicons (CC-BY / CC-0)', 8, 'rgba(44,62,80,0.35)')

# ===== SAVE =====
d.save_svg('ms_proteomics_bioicons.svg')
print('Saved: ms_proteomics_bioicons.svg')
print(f'Size: {W}x{H}')
print('Icons embedded: 20 bioicons from bioicons.com')
