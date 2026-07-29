# ProteoViz

Drop your protein quantification table. Get publication-ready figures.

Built with **FastHTML** — Python full-stack, no JavaScript to write.

## Quick Start

```bash
pip install python-fasthtml pandas plotly openpyxl kaleido
python app.py
# → http://localhost:5001
```

## Supported Input

| Software | File | Auto-detected |
|----------|------|---------------|
| MaxQuant | `proteinGroups.txt` | ✅ |
| Spectronaut | protein/peptide export | ✅ |
| DIA-NN | report.tsv | ✅ |
| Generic | CSV/Excel (ID + log2FC + p-value) | ✅ |

## Features

- **Volcano plot** — interactive Plotly.js, top hits labeled, export PNG (300 DPI) / PDF
- **Heatmap** — top differentially abundant proteins, red-blue gradient
- **Top hits table** — sortable, exportable to CSV
- **Zero config** — auto-detects protein ID, log2FC, and p-value columns
- **Handles any proteomics software output**

## Sample Data

```bash
python app.py
# → Open http://localhost:5001 → Upload sample_data.csv
```

## Tech Stack

- **FastHTML** — Python web framework (Starlette + HTMX + fastcore FT)
- **Plotly.js** — client-side interactive charts (CDN)
- **Plotly.py** — server-side figure generation → JSON
- **Pandas** — data processing
