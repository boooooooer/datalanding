"""
ProteoViz — Zero-config differential proteomics visualization.
FastHTML edition. Drop your protein quantification table → volcano plot + heatmap.
"""
from fasthtml.common import *
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import json
from io import BytesIO
import uuid

# ═══════════════════════════════════════════════
# App Setup
# ═══════════════════════════════════════════════
app, rt = fast_app(
    hdrs=[Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js")],
)

# ═══════════════════════════════════════════════
# Server-side data store (keyed by session)
# ═══════════════════════════════════════════════
user_store = {}

def get_store(session):
    sid = session.setdefault('uid', str(uuid.uuid4()))
    if sid not in user_store:
        user_store[sid] = {}
    return user_store[sid]

# ═══════════════════════════════════════════════
# Core Logic
# ═══════════════════════════════════════════════
def detect_columns(df):
    """Auto-detect protein ID, log2FC, p-value columns."""
    cols = df.columns.tolist()
    result = {"id": None, "fc": None, "pval": None}
    for c in cols:
        cl = c.lower().replace(" ", "_").replace(".", "_")
        if result["id"] is None and any(k in cl for k in
            ["protein_id", "protein_ids", "pg_protein", "protein_group",
             "uniprot", "accession", "gene_name", "gene_symbol", "entry"]):
            result["id"] = c
        if result["fc"] is None and any(k in cl for k in
            ["log2_fc", "log2fc", "log_fc", "logfc", "fold_change",
             "log2_fold_change", "ratio", "diff", "avg_log2fc"]):
            if c != result["id"]:
                result["fc"] = c
        if result["pval"] is None and any(k in cl for k in
            ["p_value", "pvalue", "p_val", "pval", "adj_p", "padj",
             "fdr", "q_value", "qvalue", "moderated_p"]):
            if c not in [result["id"], result["fc"]]:
                result["pval"] = c
    return result

def process_data(df, col_map, fc_cutoff, p_cutoff):
    """Extract, clean, and classify data."""
    sub = df[[col_map["id"], col_map["fc"], col_map["pval"]]].copy()
    sub.columns = ["Protein", "log2FC", "pvalue"]
    sub["log2FC"] = pd.to_numeric(sub["log2FC"], errors="coerce")
    sub["pvalue"] = pd.to_numeric(sub["pvalue"], errors="coerce")
    sub = sub.dropna(subset=["log2FC", "pvalue"])
    sub["-log10(p)"] = -np.log10(sub["pvalue"].clip(lower=1e-300))
    sub["significant"] = "NS"

    up_mask = (sub["log2FC"] >= fc_cutoff) & (sub["pvalue"] < p_cutoff)
    down_mask = (sub["log2FC"] <= -fc_cutoff) & (sub["pvalue"] < p_cutoff)
    sub.loc[up_mask, "significant"] = "Up"
    sub.loc[down_mask, "significant"] = "Down"
    return sub

# ═══════════════════════════════════════════════
# Plot Generators → Plotly JSON
# ═══════════════════════════════════════════════
def volcano_fig(data, fc_cutoff, p_cutoff):
    colors = {"Up": "#C44E52", "Down": "#4C72B0", "NS": "#B0B0B0"}
    n_up = int((data["significant"] == "Up").sum())
    n_down = int((data["significant"] == "Down").sum())

    fig = px.scatter(
        data, x="log2FC", y="-log10(p)", color="significant",
        color_discrete_map=colors, hover_name="Protein",
        hover_data={"log2FC": ":.3f", "pvalue": ":.2e", "-log10(p)": False},
        title=f"Volcano Plot — {n_up} up, {n_down} down", opacity=0.6,
    )
    fig.update_traces(marker=dict(size=6, line=dict(width=0)))
    fig.add_hline(y=-np.log10(p_cutoff), line_dash="dash", line_color="gray",
                   opacity=0.5, annotation_text=f"p={p_cutoff}")
    fig.add_vline(x=fc_cutoff, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=-fc_cutoff, line_dash="dash", line_color="gray", opacity=0.5)

    top_up = data[data["significant"] == "Up"].nlargest(5, "-log10(p)")
    top_down = data[data["significant"] == "Down"].nlargest(5, "-log10(p)")
    for _, row in pd.concat([top_up, top_down]).iterrows():
        fig.add_annotation(
            x=row["log2FC"], y=row["-log10(p)"], text=row["Protein"],
            showarrow=True, arrowhead=2, font=dict(size=9), ax=20, ay=-20,
        )
    fig.update_layout(
        template="plotly_white", height=600,
        xaxis_title="log2 Fold Change", yaxis_title="-log10(p-value)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig

def heatmap_fig(data, top_n=50):
    sig = data[data["significant"].isin(["Up", "Down"])].nlargest(top_n, "-log10(p)")
    if len(sig) < 2:
        return None
    heat_arr = sig[["log2FC"]].values
    labels = sig["Protein"].tolist()
    fig = go.Figure(data=go.Heatmap(
        z=heat_arr, x=["log2FC"], y=labels, colorscale="RdBu_r", zmid=0,
        text=[[f"{v:.2f}"] for v in heat_arr.flatten()],
        texttemplate="%{text}", textfont={"size": 9},
        colorbar=dict(title="log2FC"),
    ))
    fig.update_layout(
        template="plotly_white", height=max(400, len(sig) * 18),
        margin=dict(l=200, r=20, t=20, b=20),
    )
    return fig

# ═══════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════
CSS = Style("""
:root {
    --primary: #2C5282; --up: #C44E52; --down: #4C72B0; --ns: #B0B0B0;
    --bg: #f5f5f5; --card-bg: #fff; --border: #e0e0e0; --text: #333; --muted: #888;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
       background: var(--bg); color: var(--text); line-height: 1.5; }
.app { display: grid; grid-template-columns: 320px 1fr; min-height: 100vh; }

/* ── Sidebar ── */
.sidebar { background: var(--card-bg); border-right: 1px solid var(--border);
           padding: 20px 24px; overflow-y: auto; max-height: 100vh; position: sticky; top: 0; }
.sidebar h2 { font-size: 13px; text-transform: uppercase; color: var(--muted);
              margin: 20px 0 8px; letter-spacing: 0.5px; }
.sidebar h2:first-child { margin-top: 0; }
.sidebar .logo { font-size: 18px; font-weight: 700; color: var(--primary); margin-bottom: 4px; }
.sidebar .logo-sub { font-size: 12px; color: var(--muted); margin-bottom: 18px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 4px; color: #555; }
.form-group select, .form-group input {
    width: 100%; padding: 8px 10px; border: 1px solid #d0d0d0;
    border-radius: 6px; font-size: 13px; background: #fafafa; }
.form-group input[type=range] { padding: 0; accent-color: var(--primary); }
.form-group .range-val { font-size: 12px; color: var(--primary); font-weight: 600; text-align: right; }
.btn { display: inline-block; padding: 8px 16px; border-radius: 6px; font-size: 14px;
       cursor: pointer; border: none; font-weight: 600; transition: background 0.15s; text-decoration: none; }
.btn-primary { background: var(--primary); color: #fff; }
.btn-primary:hover { background: #1a3a5c; }
.btn-sm { padding: 5px 10px; font-size: 12px; }
.btn-outline { background: #fff; border: 1px solid #d0d0d0; color: #555; }
.btn-outline:hover { background: #f0f0f0; }
.export-btns { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px; }

/* ── Main ── */
.main { padding: 24px 32px; overflow-y: auto; }
.main .title { font-size: 24px; font-weight: 700; color: var(--primary); margin-bottom: 2px; }
.main .subtitle { color: var(--muted); margin-bottom: 24px; font-size: 14px; }

/* ── Metric cards ── */
.metrics { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; }
.metric-card { background: var(--card-bg); border-radius: 8px; padding: 16px 20px;
               min-width: 130px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.metric-card .value { font-size: 26px; font-weight: 700; color: var(--primary); }
.metric-card .label { font-size: 11px; color: var(--muted); text-transform: uppercase;
                      letter-spacing: 0.3px; }

/* ── Tabs (JS-driven) ── */
.tab-bar { display: flex; gap: 0; border-bottom: 2px solid var(--border); margin-bottom: 16px; }
.tab-label { padding: 10px 20px; cursor: pointer; font-size: 14px; color: var(--muted);
             border-bottom: 2px solid transparent; margin-bottom: -2px;
             transition: all 0.15s; user-select: none; }
.tab-label:hover { color: var(--primary); }
.tab-label.active { color: var(--primary); border-bottom-color: var(--primary); font-weight: 600; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }

/* ── Plot containers ── */
.plot-box { background: var(--card-bg); border-radius: 8px; padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin-bottom: 16px; }
.plot-box h3 { font-size: 16px; color: var(--primary); margin-bottom: 12px; }

/* ── Tables ── */
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; background: var(--card-bg);
              border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.data-table th { background: #f8f9fa; padding: 10px 12px; text-align: left; font-weight: 600;
                 border-bottom: 2px solid var(--border); position: sticky; top: 0; }
.data-table td { padding: 8px 12px; border-bottom: 1px solid #f0f0f0; }
.data-table tr:hover td { background: #fafbfc; }
.table-wrap { max-height: 500px; overflow-y: auto; border-radius: 8px;
              box-shadow: 0 1px 3px rgba(0,0,0,0.06); }

/* ── Upload hero ── */
.upload-hero { max-width: 560px; margin: 0 auto; text-align: center; }
.upload-hero h1 { font-size: 28px; color: var(--primary); margin-bottom: 6px; }
.upload-hero .sub { color: var(--muted); margin-bottom: 28px; font-size: 15px; }
.upload-hero .formats { text-align: left; margin-top: 24px; font-size: 14px; color: #666; }
.upload-hero .formats ul { margin: 8px 0 0 20px; }
.upload-hero .formats li { margin-bottom: 4px; }

/* ── Upload page layout ── */
.upload-page { display: flex; align-items: center; justify-content: center;
               min-height: 100vh; padding: 40px 20px; }
.upload-card { background: var(--card-bg); border-radius: 12px; padding: 40px;
               box-shadow: 0 2px 12px rgba(0,0,0,0.08); max-width: 560px; width: 100%; }
""")

# ═══════════════════════════════════════════════
# UI Components
# ═══════════════════════════════════════════════

def upload_page(error=None):
    """Landing page — file upload only."""
    err_msg = P(error, style="color:#C44E52; margin-bottom:16px;") if error else ""
    return (
        CSS,
        Title("ProteoViz"),
        Div(cls="upload-page")(
            Div(cls="upload-card")(
                H1("🧬 ProteoViz", style="font-size:28px;color:#2C5282;text-align:center;"),
                P("Drop your quantification table. Get publication-ready figures.",
                  style="color:#888;text-align:center;margin-bottom:28px;"),
                err_msg,
                Form(action="/upload", method="post", enctype="multipart/form-data")(
                    Input(type="file", name="file",
                          accept=".csv,.tsv,.txt,.xlsx,.xls",
                          style="width:100%;padding:12px;border:2px dashed #d0d0d0;border-radius:8px;margin-bottom:16px;"),
                    Button("Upload & Analyze", type="submit",
                           style="width:100%;padding:12px;background:#2C5282;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;"),
                ),
                Div(cls="formats")(
                    H3("Supported formats", style="font-size:14px;margin-top:20px;"),
                    Ul(
                        Li(B("MaxQuant"), " proteinGroups.txt"),
                        Li(B("Spectronaut"), " peptide/protein export"),
                        Li(B("DIA-NN"), " report"),
                        Li("Generic CSV/Excel — Protein ID + log2FC + p-value"),
                    ),
                    P("Columns are auto-detected. You can override after upload.",
                      style="color:#888;font-size:13px;margin-top:12px;"),
                ),
            ),
        ),
    )

def sidebar(s, cols, col_map, fc_cutoff, p_cutoff):
    """Render the sidebar with controls. Each change triggers htmx POST to /update."""
    def sel(name, current_val):
        opts = [Option(c, value=c, selected=(c == current_val)) for c in cols]
        return Select(
            *opts,
            name=name, id=f"sel-{name}",
            hx_post="/update", hx_target=".main", hx_trigger="change",
        )

    return Div(cls="sidebar")(
        Div(cls="logo")("🧬 ProteoViz"),
        Div(cls="logo-sub")("Differential Proteomics Visualization"),

        H2("1. Data"),
        P(f"{s.get('n_rows','?')} rows × {len(cols)} cols loaded", style="font-size:12px;color:#888;"),

        Form(id="sidebar-form")(
            H2("2. Map Columns"),
            Div(cls="form-group")(
                Label("Protein ID", _for="sel-id"),
                sel("id", col_map["id"]),
            ),
            Div(cls="form-group")(
                Label("log2 Fold Change", _for="sel-fc"),
                sel("fc", col_map["fc"]),
            ),
            Div(cls="form-group")(
                Label("p-value / FDR", _for="sel-pval"),
                sel("pval", col_map["pval"]),
            ),

            H2("3. Thresholds"),
            Div(cls="form-group")(
                Label("|log2 FC| cutoff"),
                Input(type="range", name="fc_cutoff", min="0", max="3", step="0.1",
                      value=str(fc_cutoff),
                      hx_post="/update", hx_target=".main", hx_trigger="change",
                      oninput="this.nextElementSibling.textContent=this.value"),
                Div(cls="range-val")(str(fc_cutoff)),
            ),
            Div(cls="form-group")(
                Label("p-value cutoff"),
                Select(
                    Option("0.05", value="0.05", selected=(p_cutoff == 0.05)),
                    Option("0.01", value="0.01", selected=(p_cutoff == 0.01)),
                    Option("0.001", value="0.001", selected=(p_cutoff == 0.001)),
                    Option("0.0001", value="0.0001", selected=(p_cutoff == 0.0001)),
                    name="p_cutoff",
                    hx_post="/update", hx_target=".main", hx_trigger="change",
                ),
            ),
        ),

        H2("4. Export"),
        Div(cls="export-btns")(
            A("Volcano PNG", href="/download/volcano-png", cls="btn btn-outline btn-sm"),
            A("Volcano PDF", href="/download/volcano-pdf", cls="btn btn-outline btn-sm"),
            A("Top Hits CSV", href="/download/tophits-csv", cls="btn btn-outline btn-sm"),
        ),
    )

def main_content(data, fc_cutoff, p_cutoff):
    """Render the main content area: metrics + tabs with plots/table."""
    n_total = len(data)
    n_up = int((data["significant"] == "Up").sum())
    n_down = int((data["significant"] == "Down").sum())

    # Plots
    v_json = json.dumps(pio.to_json(volcano_fig(data, fc_cutoff, p_cutoff)))
    h_fig = heatmap_fig(data)
    h_json = json.dumps(pio.to_json(h_fig)) if h_fig else "null"

    # Top hits table
    top_df = data[data["significant"].isin(["Up", "Down"])].nlargest(50, "-log10(p)")
    top_rows = []
    for _, row in top_df.iterrows():
        top_rows.append(Tr(
            Td(row["Protein"]),
            Td(f"{row['log2FC']:.3f}"),
            Td(f"{row['pvalue']:.2e}"),
            Td(f"{row['-log10(p)']:.2f}"),
            Td(Span(row["significant"],
                    style=f"color:{'#C44E52' if row['significant']=='Up' else '#4C72B0'};font-weight:600;")),
        ))

    # Raw data table (first 200 rows)
    raw_rows = []
    for _, row in data.head(200).iterrows():
        raw_rows.append(Tr(
            Td(row["Protein"]),
            Td(f"{row['log2FC']:.3f}"),
            Td(f"{row['pvalue']:.2e}"),
            Td(f"{row['-log10(p)']:.2f}"),
            Td(row["significant"]),
        ))

    return Div(id="main-content")(
        Div(cls="title")("ProteoViz Results"),
        Div(cls="subtitle")(f"Showing {n_up} up-regulated, {n_down} down-regulated proteins"),

        # ── Metric Cards ──
        Div(cls="metrics")(
            Div(cls="metric-card")(Div(cls="value")(f"{n_total:,}"), Div(cls="label")("Total Proteins")),
            Div(cls="metric-card")(Div(cls="value", style="color:#C44E52;")(str(n_up)),
                                   Div(cls="label")(f"Up-regulated ({n_up/max(n_total,1)*100:.1f}%)")),
            Div(cls="metric-card")(Div(cls="value", style="color:#4C72B0;")(str(n_down)),
                                   Div(cls="label")(f"Down-regulated ({n_down/max(n_total,1)*100:.1f}%)")),
            Div(cls="metric-card")(Div(cls="value")(str(fc_cutoff)), Div(cls="label")("|log2FC| cutoff")),
            Div(cls="metric-card")(Div(cls="value")(str(p_cutoff)), Div(cls="label")("p cutoff")),
        ),

        # ── Tabs ──
        Div(cls="tab-bar")(
            Label("Volcano Plot", cls="tab-label active", onclick="switchTab('volcano')"),
            Label("Heatmap", cls="tab-label", onclick="switchTab('heatmap')"),
            Label("Top Hits", cls="tab-label", onclick="switchTab('tophits')"),
            Label("Raw Data", cls="tab-label", onclick="switchTab('raw')"),
        ),
        Div(id="panel-volcano", cls="tab-panel active")(
            Div(cls="plot-box")(Div(id="volcano-plot", style="width:100%;")),
            Script(f"Plotly.newPlot('volcano-plot', {v_json})"),
        ),
        Div(id="panel-heatmap", cls="tab-panel")(
            Div(cls="plot-box")(
                Div(id="heatmap-plot", style="width:100%;"),
                P("Top differentially abundant proteins. Red = up, Blue = down.",
                  style="color:#888;font-size:12px;margin-top:8px;"),
            ),
            Script(f"Plotly.newPlot('heatmap-plot', {h_json})") if h_json else P("Not enough significant proteins for heatmap.",
                  style="color:#888;padding:20px;"),
        ),
        Div(id="panel-tophits", cls="tab-panel")(
            Div(cls="table-wrap")(
                Table(cls="data-table")(
                    Thead(Tr(Th("Protein"), Th("log2FC"), Th("p-value"), Th("-log10(p)"), Th("Direction"))),
                    Tbody(*top_rows),
                ),
            ),
        ),
        Div(id="panel-raw", cls="tab-panel")(
            P(f"Showing first 200 of {n_total:,} rows.", style="color:#888;font-size:12px;margin-bottom:8px;"),
            Div(cls="table-wrap")(
                Table(cls="data-table")(
                    Thead(Tr(Th("Protein"), Th("log2FC"), Th("p-value"), Th("-log10(p)"), Th("Significant"))),
                    Tbody(*raw_rows),
                ),
            ),
        ),
        Script("""
function switchTab(name) {
    document.querySelectorAll('.tab-label').forEach(l => l.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelector('.tab-label[onclick*="' + name + '"]').classList.add('active');
    document.getElementById('panel-' + name).classList.add('active');
}
"""),
    )

def full_page(s, session):
    """Full app layout: sidebar + main."""
    cols = s['cols']
    col_map = s['col_map']
    fc_cutoff = s.get('fc_cutoff', 1.0)
    p_cutoff = s.get('p_cutoff', 0.05)

    data = process_data(s['df'], col_map, fc_cutoff, p_cutoff)
    # Cache processed data for download routes (keyed by session)
    s['_data'] = data
    s['_fc'] = fc_cutoff
    s['_p'] = p_cutoff

    return (
        CSS,
        Title("ProteoViz"),
        Div(cls="app")(
            sidebar(s, cols, col_map, fc_cutoff, p_cutoff),
            Div(cls="main")(main_content(data, fc_cutoff, p_cutoff)),
        ),
    )

# ═══════════════════════════════════════════════
# Routes
# ═══════════════════════════════════════════════

@rt("/")
def get(session):
    s = get_store(session)
    if s.get('df') is None:
        return upload_page()
    return full_page(s, session)


@rt("/upload")
async def post(session, file: UploadFile):
    s = get_store(session)
    try:
        content = await file.read()
        fname = file.filename.lower()
        if fname.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(BytesIO(content))
        elif fname.endswith(('.tsv', '.txt')):
            df = pd.read_csv(BytesIO(content), sep='\t')
        else:
            df = pd.read_csv(BytesIO(content))

        s['df'] = df
        s['n_rows'] = len(df)
        cols = df.columns.tolist()
        s['cols'] = cols

        auto = detect_columns(df)
        s['col_map'] = {
            'id': auto['id'] or cols[0],
            'fc': auto['fc'] or (cols[1] if len(cols) > 1 else cols[0]),
            'pval': auto['pval'] or (cols[2] if len(cols) > 2 else cols[0]),
        }
        s['fc_cutoff'] = 1.0
        s['p_cutoff'] = 0.05

    except Exception as e:
        return upload_page(error=f"Failed to parse file: {e}")

    # Redirect to GET / to show full app (regular redirect, not htmx)
    return RedirectResponse("/", status_code=303)


@rt("/update")
async def post(session,
               id: str = "", fc: str = "", pval: str = "",
               fc_cutoff: float = 1.0, p_cutoff: float = 0.05):
    s = get_store(session)
    if s.get('df') is None:
        return P("No data loaded. Please upload a file first.")

    # Update stored settings
    s['col_map'] = {'id': id, 'fc': fc, 'pval': pval}
    s['fc_cutoff'] = fc_cutoff
    s['p_cutoff'] = p_cutoff

    data = process_data(s['df'], s['col_map'], fc_cutoff, p_cutoff)
    s['_data'] = data
    s['_fc'] = fc_cutoff
    s['_p'] = p_cutoff

    return main_content(data, fc_cutoff, p_cutoff)


@rt("/download/volcano-png")
async def get(session):
    s = get_store(session)
    data = s.get('_data')
    if data is None:
        return "No data", 404
    fig = volcano_fig(data, s.get('_fc', 1.0), s.get('_p', 0.05))
    img = pio.to_image(fig, format="png", scale=3)
    return Response(img, media_type="image/png",
                    headers={"Content-Disposition": "attachment; filename=volcano.png"})


@rt("/download/volcano-pdf")
async def get(session):
    s = get_store(session)
    data = s.get('_data')
    if data is None:
        return "No data", 404
    fig = volcano_fig(data, s.get('_fc', 1.0), s.get('_p', 0.05))
    img = pio.to_image(fig, format="pdf")
    return Response(img, media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=volcano.pdf"})


@rt("/download/tophits-csv")
async def get(session):
    s = get_store(session)
    data = s.get('_data')
    if data is None:
        return "No data", 404
    top = data[data["significant"].isin(["Up", "Down"])].nlargest(50, "-log10(p)")
    csv = top[["Protein", "log2FC", "pvalue", "-log10(p)", "significant"]].to_csv(index=False)
    return Response(csv, media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=top_hits.csv"})


# ═══════════════════════════════════════════════
serve()
