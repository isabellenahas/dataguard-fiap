from html import escape
import textwrap

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# ================================================================
# DATAGUARD · SPRINT 4 FINAL UI
# Visual inspirado no protótipo HTML aprovado.
# Regra: HTML/CSS define aparência; CSVs definem números;
# Python/Streamlit define comportamento.
# ================================================================

st.set_page_config(
    page_title="DataGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Design tokens / CSS
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

    :root {
        --dg-bg: #0A1018;
        --dg-sidebar: #080D14;
        --dg-surface: #121B26;
        --dg-surface-hi: #16212E;
        --dg-border: rgba(141,162,185,0.16);
        --dg-border-strong: rgba(141,162,185,0.28);
        --dg-text: #E6EDF5;
        --dg-muted: #8DA2B9;
        --dg-faint: #64778C;
        --dg-accent: #22C7E8;
        --dg-accent-dim: rgba(34,199,232,0.14);
        --dg-critical: #F0554B;
        --dg-high: #F79009;
        --dg-attention: #EAB308;
        --dg-low: #12B76A;
        --dg-radius-sm: 6px;
        --dg-radius-md: 10px;
        --dg-radius-lg: 14px;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"], button, input, textarea, select {
        font-family: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif !important;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: var(--dg-bg) !important;
        color: var(--dg-text) !important;
    }

    [data-testid="stHeader"] {
        background: rgba(10,16,24,0.88) !important;
        border-bottom: 1px solid rgba(141,162,185,0.06);
    }
    #MainMenu, footer { visibility: hidden; }

    .block-container {
        max-width: 1440px;
        padding-top: 2.15rem;
        padding-bottom: 4rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--dg-sidebar) !important;
        border-right: 1px solid var(--dg-border);
        min-width: 236px !important;
        max-width: 236px !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.55rem;
    }
    .dg-brand {
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 0 8px;
        margin-bottom: 6px;
    }
    .dg-brand-mark {
        width: 9px;
        height: 9px;
        border-radius: 2px;
        background: var(--dg-accent);
        box-shadow: 0 0 0 4px var(--dg-accent-dim);
        flex: 0 0 auto;
    }
    .dg-brand-name {
        color: var(--dg-text);
        font-size: 15px;
        font-weight: 700;
        letter-spacing: .14em;
    }
    .dg-brand-sub {
        margin: 0 0 22px 8px;
        font-size: 11.5px;
        color: var(--dg-faint);
        white-space: nowrap;
    }
    .dg-side-foot {
        margin: 26px 8px 0;
        padding-top: 18px;
        border-top: 1px solid var(--dg-border);
        color: var(--dg-faint);
        font-size: 11px;
        line-height: 1.6;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 2px;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        position: relative;
        min-height: 38px;
        padding: 8px 10px 8px 22px !important;
        border-radius: var(--dg-radius-sm);
        border-left: 2px solid transparent;
        color: var(--dg-muted) !important;
        transition: background .12s ease, color .12s ease;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(141,162,185,0.07);
        color: var(--dg-text) !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label::before {
        content: "";
        position: absolute;
        left: 9px;
        top: 50%;
        transform: translateY(-50%);
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: currentColor;
        opacity: .45;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background: var(--dg-accent-dim);
        border-left-color: var(--dg-accent);
        color: var(--dg-text) !important;
        font-weight: 600;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked)::before {
        opacity: 1;
        background: var(--dg-accent);
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child,
    [data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] p {
        font-size: 13.5px !important;
    }

    /* Page header */
    .dg-page-head {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 24px;
        flex-wrap: wrap;
        padding-bottom: 18px;
        margin-bottom: 24px;
        border-bottom: 1px solid var(--dg-border);
    }
    .dg-page-title {
        margin: 0;
        color: var(--dg-text);
        font-size: 27px;
        font-weight: 600;
        letter-spacing: -.015em;
        line-height: 1.15;
    }
    .dg-page-sub {
        margin: 5px 0 0;
        color: var(--dg-muted);
        font-size: 13.5px;
    }
    .dg-window-chip {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid var(--dg-border);
        background: var(--dg-surface);
        color: var(--dg-muted);
        font-size: 12px;
        white-space: nowrap;
    }
    .dg-window-chip b { color: var(--dg-text); font-weight: 500; }

    /* KPI bands */
    .dg-group-label {
        color: var(--dg-faint);
        font-size: 11px;
        letter-spacing: .06em;
        text-transform: uppercase;
        margin-bottom: 9px;
    }
    .dg-kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0,1fr));
        gap: 14px;
        margin-bottom: 4px;
    }
    .dg-kpi-card {
        min-height: 118px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 16px 18px;
        background: var(--dg-surface);
        border: 1px solid var(--dg-border);
        border-radius: var(--dg-radius-md);
    }
    .dg-kpi-card.hero {
        background: linear-gradient(180deg,rgba(34,199,232,.07) 0%,rgba(34,199,232,0) 62%),var(--dg-surface);
        border-color: rgba(34,199,232,.32);
    }
    .dg-kpi-card.context { background: transparent; }
    .dg-kpi-card.small { min-height: 96px; }
    .dg-kpi-label {
        display: flex;
        align-items: center;
        gap: 6px;
        color: var(--dg-muted);
        font-size: 12.5px;
    }
    .dg-kpi-card.hero .dg-kpi-label { color: var(--dg-text); }
    .dg-kpi-card.context .dg-kpi-label { color: var(--dg-faint); }
    .dg-kpi-value {
        margin-top: 10px;
        color: var(--dg-text);
        font-size: 34px;
        line-height: 1.1;
        font-weight: 600;
        font-variant-numeric: tabular-nums;
        letter-spacing: -.025em;
    }
    .dg-kpi-card.hero .dg-kpi-value { color: var(--dg-accent); font-size: 48px; }
    .dg-kpi-card.context .dg-kpi-value { font-size: 27px; }
    .dg-kpi-card.small .dg-kpi-value { font-size: 26px; margin-top: 6px; }
    .dg-kpi-unit {
        margin-left: 6px;
        color: var(--dg-faint);
        font-size: 13px;
        font-weight: 400;
        letter-spacing: 0;
    }
    .dg-kpi-foot {
        margin-top: 9px;
        color: var(--dg-faint);
        font-size: 11.5px;
    }
    .dg-risk-dot {
        width: 7px; height: 7px; border-radius: 50%;
        background: var(--dg-critical); display: inline-block;
    }
    .dg-prio-tag {
        display: inline-block;
        padding: 1px 5px;
        border-radius: 4px;
        border: 1px solid var(--dg-border);
        color: var(--dg-faint);
        font-size: 10.5px;
        font-weight: 600;
    }

    /* Sections */
    .dg-section { margin-top: 30px; }
    .dg-section-head {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 13px;
    }
    .dg-section-title {
        margin: 0;
        color: var(--dg-text);
        font-size: 16px;
        font-weight: 600;
    }
    .dg-section-sub {
        margin: 2px 0 0;
        color: var(--dg-muted);
        font-size: 12.5px;
    }
    .dg-caption {
        margin: 11px 0 0;
        max-width: 86ch;
        color: var(--dg-faint);
        font-size: 12px;
        line-height: 1.6;
    }

    /* Notes */
    .dg-note {
        display: flex;
        gap: 12px;
        margin-top: 22px;
        padding: 14px 16px;
        max-width: 86ch;
        background: var(--dg-surface);
        border: 1px solid var(--dg-border);
        border-left: 2px solid var(--dg-accent);
        border-radius: var(--dg-radius-sm);
        color: var(--dg-muted);
        font-size: 13px;
        line-height: 1.55;
    }
    .dg-note.warn { border-left-color: var(--dg-attention); }
    .dg-note b { color: var(--dg-text); font-weight: 500; }

    /* Cards wrapping Plotly */
    .dg-chart-label {
        margin: 0 0 -4px;
        padding: 17px 20px 0;
        border: 1px solid var(--dg-border);
        border-bottom: 0;
        border-radius: var(--dg-radius-md) var(--dg-radius-md) 0 0;
        background: var(--dg-surface);
    }
    .dg-chart-shell + div [data-testid="stPlotlyChart"] {
        margin-top: 0 !important;
    }
    [data-testid="stPlotlyChart"] {
        border: 1px solid var(--dg-border);
        border-radius: 0 0 var(--dg-radius-md) var(--dg-radius-md);
        background: var(--dg-surface);
        padding: 0 6px 8px;
    }

    /* Tables */
    .dg-table-wrap {
        overflow-x: auto;
        border: 1px solid var(--dg-border);
        border-radius: var(--dg-radius-md);
        background: var(--dg-surface);
    }
    .dg-table {
        width: 100%;
        border-collapse: collapse;
        color: var(--dg-text);
        font-size: 13px;
    }
    .dg-table thead th {
        padding: 10px 14px;
        background: var(--dg-surface-hi);
        border-bottom: 1px solid var(--dg-border);
        color: var(--dg-muted);
        font-size: 11.5px;
        font-weight: 500;
        text-align: left;
        white-space: nowrap;
    }
    .dg-table thead th.right, .dg-table td.right { text-align: right; }
    .dg-table tbody td {
        padding: 9px 14px;
        border-bottom: 1px solid rgba(141,162,185,.08);
        vertical-align: middle;
    }
    .dg-table tbody tr:last-child td { border-bottom: 0; }
    .dg-table tbody tr:hover { background: rgba(141,162,185,.04); }
    .dg-table tbody tr.selected { background: rgba(34,199,232,.07); }
    .dg-dim { color: var(--dg-muted); }
    .dg-best { color: var(--dg-accent); font-weight: 600; }
    .dg-pick {
        margin-left: 7px;
        padding: 1px 6px;
        border: 1px solid rgba(34,199,232,.4);
        border-radius: 4px;
        color: var(--dg-accent);
        font-size: 10px;
        font-weight: 600;
    }
    .dg-band {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 2px 9px;
        border-radius: 999px;
        font-size: 11.5px;
        font-weight: 600;
        white-space: nowrap;
    }
    .dg-band::before {
        content: ""; width: 6px; height: 6px; border-radius: 50%; background: currentColor;
    }
    .dg-band.critical { color: var(--dg-critical); background: rgba(240,85,75,.11); }
    .dg-band.high { color: var(--dg-high); background: rgba(247,144,9,.11); }
    .dg-band.attention { color: var(--dg-attention); background: rgba(234,179,8,.11); }
    .dg-band.low { color: var(--dg-low); background: rgba(18,183,106,.11); }
    .dg-score { display: flex; align-items: center; gap: 9px; justify-content: flex-end; }
    .dg-score-bar { width: 52px; height: 4px; background: rgba(141,162,185,.14); border-radius: 2px; overflow: hidden; }
    .dg-score-fill { height: 100%; background: var(--dg-critical); }

    /* Streamlit widgets */
    [data-testid="stMultiSelect"] > div > div,
    [data-baseweb="select"] > div {
        background: var(--dg-surface) !important;
        border-color: var(--dg-border-strong) !important;
        border-radius: var(--dg-radius-sm) !important;
        color: var(--dg-text) !important;
    }
    [data-baseweb="tag"] {
        background: var(--dg-accent-dim) !important;
        color: var(--dg-text) !important;
    }
    [data-testid="stWidgetLabel"] p {
        color: var(--dg-muted) !important;
        font-size: 11.5px !important;
    }

    /* KPI & Action */
    .dg-prio-head {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 22px 0 11px;
        color: var(--dg-muted);
        font-size: 13px;
    }
    .dg-prio-head span { color: var(--dg-text); font-size: 15px; font-weight: 600; }
    .dg-prio-head hr { flex: 1; border: 0; border-top: 1px solid var(--dg-border); }
    .dg-target-row { display:flex; align-items:center; gap:8px; margin-top:10px; flex-wrap:wrap; }
    .dg-target-chip {
        padding: 2px 9px; border: 1px solid var(--dg-border-strong); border-radius:999px;
        color: var(--dg-muted); font-size:11.5px;
    }
    .dg-target-chip b { color: var(--dg-text); font-weight:500; }
    .dg-status { padding:2px 9px; border-radius:999px; font-size:11.5px; font-weight:600; }
    .dg-status.ok { color:var(--dg-low); background:rgba(18,183,106,.11); }
    .dg-status.watch { color:var(--dg-attention); background:rgba(234,179,8,.11); }

    .dg-rec-card {
        overflow: hidden;
        border: 1px solid var(--dg-border);
        border-radius: var(--dg-radius-md);
        background: var(--dg-surface);
    }
    .dg-rec {
        display: flex; gap:16px; padding:18px; border-bottom:1px solid var(--dg-border);
    }
    .dg-rec:last-child { border-bottom:0; }
    .dg-rec-rank {
        width:26px; height:26px; flex:0 0 26px; border-radius:50%;
        display:grid; place-items:center; margin-top:1px;
        background:var(--dg-accent-dim); color:var(--dg-accent);
        font-size:12.5px; font-weight:600;
    }
    .dg-rec-title { margin:0 0 6px; color:var(--dg-text); font-size:14.5px; font-weight:600; }
    .dg-rec-evidence { margin:0; color:var(--dg-muted); font-size:13px; max-width:86ch; }
    .dg-rec-action {
        margin:10px 0 0; padding-left:12px; border-left:2px solid var(--dg-border-strong);
        color:var(--dg-text); font-size:13px; max-width:86ch;
    }
    .dg-rec-action span { display:block; margin-bottom:2px; color:var(--dg-faint); font-size:11px; }

    /* Status chips */
    .dg-status-row { display:flex; flex-wrap:wrap; gap:8px; margin:0 0 24px; }
    .dg-mini-chip {
        display:inline-flex; align-items:center; gap:6px; padding:5px 9px;
        border:1px solid var(--dg-border); border-radius:999px;
        background:rgba(18,27,38,.6); color:var(--dg-muted); font-size:11.5px;
    }
    .dg-mini-chip i { width:6px; height:6px; border-radius:50%; background:var(--dg-low); display:inline-block; }

    @media (max-width: 1100px) {
        .dg-kpi-grid { grid-template-columns: repeat(2,minmax(0,1fr)); }
    }
    @media (max-width: 700px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .dg-kpi-grid { grid-template-columns: 1fr; }
        .dg-page-title { font-size: 24px; }
        .dg-kpi-card.hero .dg-kpi-value { font-size: 40px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Data
# -----------------------------
@st.cache_data
def carregar_dados():
    historico = pd.read_csv("outputs/historico_diario.csv", parse_dates=["Data"])
    previsao = pd.read_csv("outputs/previsao_d7.csv", parse_dates=["Data"])
    ola = pd.read_csv("outputs/ranking_ola.csv", parse_dates=["Aberto"])
    patterns = pd.read_csv("outputs/patterns_ic.csv")
    grupos = pd.read_csv("outputs/grupos.csv")
    metricas_forecast = pd.read_csv("outputs/metricas_forecast.csv")
    metricas_ola = pd.read_csv("outputs/metricas_ola.csv")
    kpi = pd.read_csv("outputs/kpi_2025.csv")
    previsao_prioridades = pd.read_csv("outputs/previsao_prioridades_d7.csv", parse_dates=["Data"])
    recomendacoes = pd.read_csv("outputs/recomendacoes_operacionais.csv")
    return (
        historico, previsao, ola, patterns, grupos,
        metricas_forecast, metricas_ola, kpi,
        previsao_prioridades, recomendacoes,
    )

(
    historico, previsao, ola, patterns, grupos,
    metricas_forecast, metricas_ola, kpi,
    previsao_prioridades, recomendacoes,
) = carregar_dados()

# -----------------------------
# Helpers
# -----------------------------
ACCENT = "#22C7E8"
MUTED_BLUE = "#7FA8D0"
BG = "#0A1018"
SURFACE = "#121B26"
TEXT = "#E6EDF5"
MUTED = "#8DA2B9"
FAINT = "#64778C"
GRID = "rgba(141,162,185,0.10)"


def fmt_int(value):
    return f"{int(round(float(value))):,}".replace(",", ".")


def fmt_num(value, dec=2):
    return f"{float(value):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _html_fragment(value):
    """Compacta HTML antes de entregar ao Markdown do Streamlit."""
    return " ".join(textwrap.dedent(str(value)).strip().splitlines())


def render_html(value):
    st.markdown(_html_fragment(value), unsafe_allow_html=True)


def page_header(title, subtitle, chip_html):
    render_html(
        f"""
        <div class="dg-page-head">
          <div>
            <h1 class="dg-page-title">{escape(title)}</h1>
            <p class="dg-page-sub">{escape(subtitle)}</p>
          </div>
          <div class="dg-window-chip">{chip_html}</div>
        </div>
        """
    )


def section_header(title, subtitle=None):
    sub = f'<p class="dg-section-sub">{escape(subtitle)}</p>' if subtitle else ""
    render_html(
        f"""
        <div class="dg-section-head">
          <div>
            <h2 class="dg-section-title">{escape(title)}</h2>
            {sub}
          </div>
        </div>
        """
    )


def note(text, bold=None, warn=False, top=True):
    cls = "dg-note warn" if warn else "dg-note"
    style = "" if top else ' style="margin-top:0"'
    prefix = f"<b>{escape(bold)}</b> " if bold else ""
    render_html(f'<div class="{cls}"{style}><span>{prefix}{text}</span></div>')


def kpi_grid(cards):
    parts = ['<div class="dg-kpi-grid">']
    for c in cards:
        classes = ["dg-kpi-card"]
        if c.get("hero"):
            classes.append("hero")
        if c.get("context"):
            classes.append("context")
        if c.get("small"):
            classes.append("small")

        label = str(c["label"])
        if c.get("risk_dot"):
            label = '<span class="dg-risk-dot"></span>' + label
        if c.get("tag"):
            label = f'<span class="dg-prio-tag">{escape(str(c["tag"]))}</span> ' + label

        unit = (
            f'<span class="dg-kpi-unit">{escape(str(c["unit"]))}</span>'
            if c.get("unit")
            else ""
        )
        foot = escape(str(c.get("foot", "")))

        parts.append(
            f'<article class="{" ".join(classes)}">'
            f'<div>'
            f'<div class="dg-kpi-label">{label}</div>'
            f'<div class="dg-kpi-value">{c["value"]}{unit}</div>'
            f'</div>'
            f'<div class="dg-kpi-foot">{foot}</div>'
            f'</article>'
        )
    parts.append("</div>")
    render_html("".join(parts))


def chart_header(title, subtitle=None):
    sub = f'<p class="dg-section-sub">{escape(subtitle)}</p>' if subtitle else ""
    render_html(
        f"""
        <div class="dg-chart-label dg-chart-shell">
          <h2 class="dg-section-title">{escape(title)}</h2>
          {sub}
        </div>
        """
    )


def base_layout(fig, height=330, legend=True):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=24, b=14),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(family="IBM Plex Sans", color=MUTED, size=12),
        hoverlabel=dict(bgcolor="#16212E", bordercolor="#253447", font_color=TEXT),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=MUTED, size=11),
        ) if legend else dict(visible=False),
        xaxis=dict(
            title="",
            showgrid=False,
            zeroline=False,
            linecolor="rgba(141,162,185,0.10)",
            tickfont=dict(color=FAINT),
        ),
        yaxis=dict(
            title="",
            gridcolor=GRID,
            zeroline=False,
            tickfont=dict(color=FAINT),
        ),
    )
    return fig


def table_forecast(df):
    rows = []
    best = df["MAE"].astype(float).idxmin()
    for idx, row in df.iterrows():
        selected = idx == best
        cls = ' class="selected"' if selected else ""
        pick = '<span class="dg-pick">selecionado</span>' if selected else ""
        mae_cls = "dg-best" if selected else ""
        rows.append(
            f"<tr{cls}>"
            f"<td>{escape(str(row['Modelo']))}{pick}</td>"
            f"<td class='right {mae_cls}'>{fmt_num(row['MAE'])}</td>"
            f"<td class='right'>{fmt_num(row['RMSE'])}</td>"
            f"<td class='right'>{fmt_num(row['MAPE_%'])}%</td>"
            "</tr>"
        )
    return (
        '<div class="dg-table-wrap"><table class="dg-table">'
        '<thead><tr><th>Modelo</th><th class="right">MAE</th><th class="right">RMSE</th><th class="right">MAPE</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def table_ola_models(df):
    selected_name = "Logistic + Produto/Categoria"
    rows = []
    for _, row in df.iterrows():
        selected = str(row["Modelo"]) == selected_name
        cls = ' class="selected"' if selected else ""
        pick = '<span class="dg-pick">selecionado</span>' if selected else ""
        auc_cls = "dg-best" if selected else ""
        rows.append(
            f"<tr{cls}>"
            f"<td>{escape(str(row['Modelo']))}{pick}</td>"
            f"<td class='right'>{fmt_num(row['Precision'],3)}</td>"
            f"<td class='right'>{fmt_num(row['Recall'],2)}</td>"
            f"<td class='right'>{fmt_num(row['F1'],3)}</td>"
            f"<td class='right {auc_cls}'>{fmt_num(row['ROC_AUC'],3)}</td>"
            f"<td class='right {auc_cls}'>{fmt_num(row['PR_AUC'],3)}</td>"
            "</tr>"
        )
    return (
        '<div class="dg-table-wrap"><table class="dg-table">'
        '<thead><tr><th>Modelo</th><th class="right">Precision</th><th class="right">Recall</th><th class="right">F1</th><th class="right">ROC AUC</th><th class="right">PR AUC</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def risk_band_html(band):
    b = str(band).upper()
    cls = {"CRÍTICO": "critical", "ALTO": "high", "ATENÇÃO": "attention", "BAIXO": "low"}.get(b, "low")
    return f'<span class="dg-band {cls}">{escape(b)}</span>'


def ola_table(df, limit=100):
    rows = []
    for _, row in df.head(limit).iterrows():
        score = float(row["Risk_Score"])
        rows.append(
            "<tr>"
            f"<td>{escape(str(row['Número']))}</td>"
            f"<td class='dg-dim'>{escape(str(row['Prioridade']))}</td>"
            f"<td>{escape(str(row['Produto']))}</td>"
            f"<td class='dg-dim'>{escape(str(row['Categoria']))}</td>"
            f"<td>{escape(str(row['Grupo designado']))}</td>"
            f"<td class='dg-dim'>{escape(str(row['Aberto por']))}</td>"
            f"<td class='right'><div class='dg-score'><span>{fmt_num(score,1)}</span><span class='dg-score-bar'><span class='dg-score-fill' style='width:{min(max(score,0),100):.1f}%'></span></span></div></td>"
            f"<td>{risk_band_html(row['Faixa_Risco'])}</td>"
            "</tr>"
        )
    return (
        '<div class="dg-table-wrap"><table class="dg-table">'
        '<thead><tr><th>Número</th><th>Prioridade</th><th>Produto</th><th>Categoria</th><th>Grupo designado</th><th>Aberto por</th><th class="right">Risk Score</th><th>Faixa de risco</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def groups_table(df):
    rows = []
    for _, row in df.iterrows():
        rows.append(
            "<tr>"
            f"<td>{escape(str(row['Grupo designado']))}</td>"
            f"<td class='right'>{fmt_int(row['Incidentes'])}</td>"
            f"<td class='right'>{fmt_num(row['Percentual'],2)}%</td>"
            "</tr>"
        )
    return (
        '<div class="dg-table-wrap"><table class="dg-table">'
        '<thead><tr><th>Grupo designado</th><th class="right">Incidentes</th><th class="right">Participação</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def kpi_target_card(label, value, faixa, atingimento):
    status = "watch" if int(atingimento) < 100 else "ok"
    return (
        '<article class="dg-kpi-card">'
        '<div>'
        f'<div class="dg-kpi-label">{escape(str(label))}</div>'
        f'<div class="dg-kpi-value">{fmt_int(value)}</div>'
        '</div>'
        '<div class="dg-target-row">'
        f'<span class="dg-target-chip">Faixa oficial <b>{escape(str(faixa))}</b></span>'
        f'<span class="dg-status {status}">{int(atingimento)}% de atingimento</span>'
        '</div>'
        '</article>'
    )


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown(
    _html_fragment("""
    <div class="dg-brand">
      <span class="dg-brand-mark"></span>
      <span class="dg-brand-name">DATAGUARD</span>
    </div>
    <p class="dg-brand-sub">AIOps Predictive Operations</p>
    """),
    unsafe_allow_html=True,
)

pagina = st.sidebar.radio(
    "Navegação",
    ["Overview", "Predict", "OLA Risk", "Patterns", "KPI & Action"],
    label_visibility="collapsed",
)

# O Streamlit preserva a posição de rolagem entre reruns.
# Ao trocar de página, o container principal volta ao topo.
_previous_page = st.session_state.get("_dg_previous_page")
if _previous_page is None:
    st.session_state["_dg_previous_page"] = pagina
elif _previous_page != pagina:
    st.session_state["_dg_previous_page"] = pagina
    components.html(
        """
        <script>
        (function () {
            const doc = window.parent.document;
            const targets = [
                doc.querySelector('section.main'),
                doc.querySelector('[data-testid="stAppViewContainer"]'),
                doc.scrollingElement
            ];
            targets.forEach((el) => {
                if (el) {
                    try { el.scrollTop = 0; } catch (e) {}
                }
            });
            try { window.parent.scrollTo(0, 0); } catch (e) {}
        })();
        </script>
        """,
        height=0,
        width=0,
    )

st.sidebar.markdown(
    _html_fragment("""
    <div class="dg-side-foot">
      Enterprise Challenge<br>
      FIAP + Locaweb 2026
    </div>
    """),
    unsafe_allow_html=True,
)

# -----------------------------
# OVERVIEW
# -----------------------------
if pagina == "Overview":
    page_header(
        "Overview",
        "Plataforma preditiva de operações de TI",
        'Janela <b>14 dias</b> de histórico <span style="opacity:.45">|</span> projeção <b>D+7</b>',
    )

    d1 = previsao.iloc[0]["Previsao_Incidentes"]
    d7 = previsao["Previsao_Incidentes"].sum()
    criticos = int((ola["Faixa_Risco"] == "CRÍTICO").sum())

    st.markdown('<div class="dg-group-label">Projeção &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; Base histórica</div>', unsafe_allow_html=True)
    kpi_grid([
        {"label": "Previsão D+1", "value": fmt_int(d1), "unit": "incidentes", "foot": "Próximo dia operacional", "hero": True},
        {"label": "Previsão D+7", "value": fmt_int(d7), "foot": "Acumulado de 7 dias"},
        {"label": "Registros em faixa crítica", "value": fmt_int(criticos), "foot": "Acima do threshold 92,6", "context": True, "risk_dot": True},
        {"label": "Registros analisados", "value": "122.543", "foot": "Base completa do desafio", "context": True},
    ])

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    chart_header("Operação: histórico e projeção", "Incidentes por dia")

    hist = historico.tail(14)[["Data", "Volume_Total"]].copy()
    hist["Tipo"] = "Real"
    hist = hist.rename(columns={"Volume_Total": "Incidentes"})
    prev = previsao[["Data", "Previsao_Incidentes"]].copy()
    prev["Tipo"] = "Previsão"
    prev = prev.rename(columns={"Previsao_Incidentes": "Incidentes"})

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist["Data"], y=hist["Incidentes"], mode="lines+markers", name="Real",
        line=dict(color=MUTED_BLUE, width=2), marker=dict(color=MUTED_BLUE, size=5),
        hovertemplate="%{x|%d/%m}<br><b>%{y:.0f}</b> incidentes<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=prev["Data"], y=prev["Incidentes"], mode="lines+markers", name="Previsão",
        line=dict(color=ACCENT, width=2, dash="dash"), marker=dict(color=ACCENT, size=5),
        hovertemplate="%{x|%d/%m}<br><b>%{y:.0f}</b> incidentes<extra></extra>",
    ))
    fig.add_vrect(x0=prev["Data"].min(), x1=prev["Data"].max(), fillcolor="rgba(34,199,232,.05)", line_width=0, layer="below")
    fig.add_vline(x=prev["Data"].min(), line_width=1, line_dash="dot", line_color="rgba(141,162,185,.28)")
    fig.add_annotation(x=prev["Data"].min(), y=1, yref="paper", text="início da projeção", showarrow=False, xanchor="left", yanchor="bottom", font=dict(color=FAINT, size=10))
    base_layout(fig, height=340)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.markdown('</div>', unsafe_allow_html=True)

    note(
        "A modelagem prioriza o comportamento operacional recente, por isso a leitura principal parte do regime observado após setembro de 2025.",
        bold="Mudança de regime a partir de setembro de 2025.",
    )

# -----------------------------
# PREDICT
# -----------------------------
elif pagina == "Predict":
    page_header(
        "Predict",
        "Antecipação de volume operacional",
        'Método <b>média móvel 7 dias</b> <span style="opacity:.45">|</span> regime recente',
    )

    d1 = previsao.iloc[0]["Previsao_Incidentes"]
    d7 = previsao["Previsao_Incidentes"].sum()

    kpi_grid([
        {"label": "D+1", "value": fmt_int(d1), "unit": "incidentes", "foot": "Próximo dia operacional", "hero": True},
        {"label": "D+7", "value": fmt_int(d7), "unit": "incidentes", "foot": "Acumulado de 7 dias"},
        {"label": "MAPE do modelo selecionado", "value": "14,18%", "foot": "Média móvel 7d · período de validação", "context": True},
        {"label": "Critério de seleção", "value": "menor MAE", "foot": "131,69 entre 6 abordagens", "context": True},
    ])

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    section_header("Previsão por prioridade obrigatória", "P2 e P3, mesma abordagem do forecast total")
    p2_d1 = previsao_prioridades.iloc[0]["Previsao_P2"]
    p2_d7 = previsao_prioridades["Previsao_P2"].sum()
    p3_d1 = previsao_prioridades.iloc[0]["Previsao_P3"]
    p3_d7 = previsao_prioridades["Previsao_P3"].sum()
    kpi_grid([
        {"label": "D+1", "value": fmt_int(p2_d1), "tag": "P2", "small": True},
        {"label": "D+7", "value": fmt_int(p2_d7), "tag": "P2", "foot": "Acumulado", "small": True},
        {"label": "D+1", "value": fmt_int(p3_d1), "tag": "P3", "small": True},
        {"label": "D+7", "value": fmt_int(p3_d7), "tag": "P3", "foot": "Acumulado", "small": True},
    ])
    st.markdown('<p class="dg-caption">P2 e P3 usam a mesma abordagem selecionada para o forecast total: média dos últimos 7 dias do regime recente. D+7 representa o volume acumulado.</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    chart_header("Histórico recente e projeção D+7", "Incidentes por dia")
    hist = historico.tail(14)[["Data", "Volume_Total"]].copy()
    prev = previsao[["Data", "Previsao_Incidentes"]].copy()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist["Data"], y=hist["Volume_Total"], mode="lines+markers", name="Histórico", line=dict(color=MUTED_BLUE, width=2), marker=dict(size=5, color=MUTED_BLUE)))
    fig.add_trace(go.Scatter(x=prev["Data"], y=prev["Previsao_Incidentes"], mode="lines+markers", name="Previsão", line=dict(color=ACCENT, width=2, dash="dash"), marker=dict(size=5, color=ACCENT)))
    fig.add_vrect(x0=prev["Data"].min(), x1=prev["Data"].max(), fillcolor="rgba(34,199,232,.05)", line_width=0, layer="below")
    fig.add_vline(x=prev["Data"].min(), line_width=1, line_dash="dot", line_color="rgba(141,162,185,.28)")
    base_layout(fig, height=330)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    section_header("Comparação de modelos", "Período de validação, ordenado por MAE")
    st.markdown(table_forecast(metricas_forecast), unsafe_allow_html=True)
    st.markdown('<p class="dg-caption">A Média Móvel de 7 dias foi mantida porque apresentou o menor MAE entre as abordagens avaliadas. Complexidade adicional só foi mantida quando demonstrava ganho mensurável.</p></div>', unsafe_allow_html=True)

# -----------------------------
# OLA RISK
# -----------------------------
elif pagina == "OLA Risk":
    page_header(
        "OLA Risk",
        "Priorização de incidentes com maior risco operacional",
        'Modelo <b>Logistic + Produto/Categoria</b>',
    )

    criticos = int((ola["Faixa_Risco"] == "CRÍTICO").sum())
    kpi_grid([
        {"label": "Threshold crítico", "value": "92,6", "foot": "Acima deste score, faixa crítica", "hero": True},
        {"label": "Registros em faixa crítica", "value": fmt_int(criticos), "foot": "Base histórica ranqueada", "risk_dot": True},
        {"label": "Precision no threshold", "value": "20,8%", "foot": "Acerto entre os priorizados", "context": True},
        {"label": "Recall no threshold", "value": "22,0%", "foot": "Cobertura das quebras reais", "context": True},
    ])

    note(
        "O Risk Score ordena incidentes por risco. Não deve ser interpretado como probabilidade calibrada.",
        bold="Priorização relativa.", warn=True,
    )

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        prioridade = st.multiselect(
            "Prioridade",
            sorted(ola["Prioridade"].dropna().unique()),
            placeholder="Todas as prioridades",
        )
    with col2:
        faixa = st.multiselect(
            "Faixa de risco",
            ["CRÍTICO", "ALTO", "ATENÇÃO", "BAIXO"],
            default=["CRÍTICO", "ALTO"],
        )

    tabela = ola.copy()
    if prioridade:
        tabela = tabela[tabela["Prioridade"].isin(prioridade)]
    if faixa:
        tabela = tabela[tabela["Faixa_Risco"].isin(faixa)]
    tabela = tabela.sort_values("Risk_Score", ascending=False)

    st.markdown(
        f'<p class="dg-caption" style="margin:2px 0 12px">Exibindo os <b style="color:{TEXT}">100 maiores scores</b> entre {fmt_int(len(tabela))} registros filtrados.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(ola_table(tabela, 100), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    section_header("Comparação inicial dos modelos", "Avaliação antes do ajuste de threshold")
    st.markdown(table_ola_models(metricas_ola), unsafe_allow_html=True)
    st.markdown('<p class="dg-caption">Após a escolha da Logistic Regression com Produto e Categoria, o threshold operacional foi ajustado para 92,6. Nesse ponto, o objetivo deixa de ser classificar tudo e passa a ser concentrar a investigação operacional.</p></div>', unsafe_allow_html=True)

# -----------------------------
# PATTERNS
# -----------------------------
elif pagina == "Patterns":
    page_header(
        "Patterns",
        "Recorrência e concentração operacional",
        'Base <b>122.543</b> registros',
    )

    top_group = grupos.iloc[0]
    top_ic = patterns.iloc[0]
    kpi_grid([
        {"label": "Concentração da principal equipe", "value": f"{fmt_num(top_group['Percentual'],2)}%", "foot": str(top_group["Grupo designado"]), "hero": True},
        {"label": "Principal equipe", "value": escape(str(top_group["Grupo designado"])), "foot": "Maior volume atribuído"},
        {"label": "IC mais recorrente", "value": escape(str(top_ic["Item de configuração"])), "foot": f"{fmt_int(top_ic['Incidentes'])} incidentes", "context": True},
        {"label": "Itens no ranking", "value": "15", "foot": "Principais itens de configuração", "context": True},
    ])

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    chart_header("Principais itens de configuração", "Incidentes acumulados por item")
    top15 = patterns.head(15).sort_values("Incidentes", ascending=True).copy()
    colors = [ACCENT if ic == str(top_ic["Item de configuração"]) else "rgba(127,168,208,.55)" for ic in top15["Item de configuração"]]
    fig = go.Figure(go.Bar(
        x=top15["Incidentes"], y=top15["Item de configuração"], orientation="h",
        marker_color=colors,
        text=[fmt_int(v) for v in top15["Incidentes"]], textposition="outside",
        hovertemplate="<b>%{y}</b><br>%{x:.0f} incidentes<extra></extra>",
    ))
    base_layout(fig, height=470, legend=False)
    fig.update_xaxes(showgrid=True, gridcolor=GRID, tickfont=dict(color=FAINT))
    fig.update_yaxes(showgrid=False, tickfont=dict(color=MUTED))
    fig.update_traces(cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    section_header("Concentração por equipe", "Volume atribuído e participação no regime recente")
    st.markdown(groups_table(grupos), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    note(
        "P4/P5 e eventos de monitoramento foram avaliados como precursores de P2/P3. No teste de janela de 24h, o sinal simples não apresentou capacidade discriminativa e não foi incorporado ao mecanismo preditivo do MVP.",
        bold="Hipótese investigada e descartada.",
    )

# -----------------------------
# KPI & ACTION
# -----------------------------
elif pagina == "KPI & Action":
    page_header(
        "KPI & Action",
        "Leitura dos KPIs oficiais e tradução dos resultados em ação operacional",
        'Ano-base <b>2025</b>',
    )

    note(
        "segundo as faixas oficiais do desafio. Os percentuais abaixo não são probabilidades e o DataGuard não transforma o OLA Risk Score em probabilidade calibrada.",
        bold="Atingimento observado em 2025",
        top=False,
    )

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    section_header("Atingimento dos KPIs em 2025", "Valor observado contra a faixa oficial")

    for prio in ["P2", "P3"]:
        sub = kpi[kpi["Prioridade"] == prio]
        volume = sub[sub["Indicador"] == "Volume de incidentes no KPI"].iloc[0]
        olak = sub[sub["Indicador"] == "OLA quebrado"].iloc[0]
        st.markdown(f'<div class="dg-prio-head"><span>{prio}</span><hr></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="dg-kpi-grid" style="grid-template-columns:repeat(2,minmax(0,1fr))">'
            + kpi_target_card("Volume de incidentes no KPI", volume["Valor_2025"], volume["Faixa_oficial"], volume["Atingimento_%"])
            + kpi_target_card("OLA quebrado", olak["Valor_2025"], olak["Faixa_oficial"], olak["Atingimento_%"])
            + '</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    section_header("Visão D+1 e D+7 por prioridade", "Mesma projeção apresentada em Predict")
    p2_d1 = previsao_prioridades.iloc[0]["Previsao_P2"]
    p2_d7 = previsao_prioridades["Previsao_P2"].sum()
    p3_d1 = previsao_prioridades.iloc[0]["Previsao_P3"]
    p3_d7 = previsao_prioridades["Previsao_P3"].sum()
    kpi_grid([
        {"label": "D+1", "value": fmt_int(p2_d1), "tag": "P2", "small": True},
        {"label": "D+7", "value": fmt_int(p2_d7), "tag": "P2", "foot": "Acumulado", "small": True},
        {"label": "D+1", "value": fmt_int(p3_d1), "tag": "P3", "small": True},
        {"label": "D+7", "value": fmt_int(p3_d7), "tag": "P3", "foot": "Acumulado", "small": True},
    ])

    chart_header("Incidentes previstos por dia", "Projeção constante por construção do método")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=previsao_prioridades["Data"], y=previsao_prioridades["Previsao_P2"],
        mode="lines+markers", name="P2", line=dict(color=ACCENT, width=2), marker=dict(color=ACCENT, size=5),
    ))
    fig.add_trace(go.Scatter(
        x=previsao_prioridades["Data"], y=previsao_prioridades["Previsao_P3"],
        mode="lines+markers", name="P3", line=dict(color=MUTED_BLUE, width=2), marker=dict(color=MUTED_BLUE, size=5),
    ))
    base_layout(fig, height=310)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dg-section">', unsafe_allow_html=True)
    section_header("Recomendações operacionais", "Camada de decisão baseada em regras explicáveis")
    rec_html = ['<div class="dg-rec-card">']
    for _, rec in recomendacoes.sort_values("Prioridade").iterrows():
        evid = str(rec["Evidência"]).replace("3,047", "3.047")
        rec_html.append(
            '<div class="dg-rec">'
            f'<span class="dg-rec-rank">{int(rec["Prioridade"])}</span>'
            '<div>'
            f'<h3 class="dg-rec-title">{escape(str(rec["Título"]))}</h3>'
            f'<p class="dg-rec-evidence">{escape(evid)}</p>'
            f'<p class="dg-rec-action"><span>Ação</span>{escape(str(rec["Ação"]))}</p>'
            '</div>'
            '</div>'
        )
    rec_html.append("</div>")
    st.markdown("".join(rec_html), unsafe_allow_html=True)
    st.markdown('<p class="dg-caption">Nenhuma recomendação é gerada por LLM e nenhuma conclusão de sobrecarga ou headcount é inferida sem dados de capacidade.</p></div>', unsafe_allow_html=True)
