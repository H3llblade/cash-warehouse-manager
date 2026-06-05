import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ─── Base ─────────────────────────────────────────────────────────── */
* { box-sizing: border-box; }

#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"]   { display: none !important; }
[data-testid="stDecoration"]{ display: none !important; }

::-webkit-scrollbar              { width: 4px; height: 4px; }
::-webkit-scrollbar-track        { background: transparent; }
::-webkit-scrollbar-thumb        { background: #2D2D4A; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover  { background: #7C3AED; }

/* ─── App shell ─────────────────────────────────────────────────────── */
.stApp {
    background: #07070E !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

/* ─── Sidebar ───────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0A0A14 !important;
    border-right: 1px solid rgba(124,58,237,0.12) !important;
}
[data-testid="stSidebarNavLink"] {
    border-radius: 10px !important;
    margin-bottom: 3px !important;
    font-weight: 500 !important;
    color: #64748B !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background: rgba(124,58,237,0.1) !important;
    color: #C4B5FD !important;
}
[data-testid="stSidebarNavLink"][aria-selected="true"] {
    background: rgba(124,58,237,0.16) !important;
    color: #A78BFA !important;
    border-left: 3px solid #7C3AED !important;
}

/* ─── Typography ────────────────────────────────────────────────────── */
h1 {
    background: linear-gradient(135deg, #FFFFFF 30%, #C4B5FD) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
}
h2 { color: #E2E8F0 !important; font-weight: 700 !important; letter-spacing: -0.3px !important; }
h3 { color: #CBD5E1 !important; font-weight: 600 !important; }
hr { border-color: rgba(255,255,255,0.06) !important; margin: 1.5rem 0 !important; }

/* ─── Metrics ───────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #111120, #0D0D1A) !important;
    border: 1px solid rgba(124,58,237,0.18) !important;
    border-radius: 14px !important;
    padding: 1.25rem 1.4rem !important;
}
[data-testid="stMetricLabel"] > div {
    color: #475569 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.9px !important;
}
[data-testid="stMetricValue"] > div {
    color: #F1F5F9 !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.4px !important;
}

/* ─── Buttons ───────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.3px !important;
    padding: 0.55rem 1.5rem !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.25) !important;
    transition: all 0.22s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.4) !important;
    filter: brightness(1.08) !important;
    border: none !important;
}
.stButton > button:active  { transform: translateY(0) !important; }
.stButton > button:focus   { box-shadow: 0 0 0 3px rgba(124,58,237,0.3) !important; }

/* ─── Number Input ──────────────────────────────────────────────────── */
.stNumberInput > label {
    color: #475569 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.7px !important;
}
.stNumberInput input {
    background: #111120 !important;
    border: 1px solid rgba(124,58,237,0.2) !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    font-weight: 500 !important;
}
.stNumberInput input:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}
.stNumberInput button {
    background: #1A1A2E !important;
    border: 1px solid rgba(124,58,237,0.18) !important;
    color: #A78BFA !important;
    border-radius: 6px !important;
}
.stNumberInput button:hover { background: rgba(124,58,237,0.18) !important; }

/* ─── Selectbox ─────────────────────────────────────────────────────── */
.stSelectbox > label {
    color: #475569 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.7px !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background: #111120 !important;
    border: 1px solid rgba(124,58,237,0.2) !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}
[data-baseweb="popover"], [data-baseweb="menu"] {
    background: #12121E !important;
    border: 1px solid rgba(124,58,237,0.18) !important;
    border-radius: 10px !important;
}
[role="option"]       { background: #12121E !important; color: #CBD5E1 !important; }
[role="option"]:hover { background: rgba(124,58,237,0.14) !important; color: #E2E8F0 !important; }

/* ─── DataFrame ─────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(124,58,237,0.12) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ─── Alerts ────────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 3px !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}

/* ─── Expander ──────────────────────────────────────────────────────── */
details {
    border: 1px solid rgba(124,58,237,0.13) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    margin-bottom: 6px !important;
    background: transparent !important;
}
summary {
    background: #10101C !important;
    padding: 13px 18px !important;
    color: #94A3B8 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    cursor: pointer !important;
    list-style: none !important;
}
summary:hover { background: rgba(124,58,237,0.08) !important; color: #E2E8F0 !important; }
details > div { background: #0D0D18 !important; padding: 16px !important; }

/* ─── Caption ───────────────────────────────────────────────────────── */
.stCaption { color: #374151 !important; font-size: 0.75rem !important; }

/* ══════════════════════════════════════════════════════════════════════
   CUSTOM COMPONENTS
   ══════════════════════════════════════════════════════════════════════ */

/* ── Page header ────────────────────────────────────────────────────── */
.cwm-page-title {
    font-size: 1.9rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF 25%, #C4B5FD);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
    margin: 0 0 4px 0;
}
.cwm-page-sub {
    font-size: 0.83rem;
    color: #475569;
    margin: 0 0 2rem 0;
    font-weight: 400;
}

/* ── Dashboard currency card ────────────────────────────────────────── */
.cwm-card {
    background: linear-gradient(145deg, #111120 0%, #0D0D1A 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 28px 22px 22px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.28s ease;
    margin-bottom: 1rem;
}
.cwm-card:hover {
    border-color: rgba(124,58,237,0.3);
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.5);
}
.cwm-card-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.cwm-card-symbol {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
    margin: 12px 0 3px;
}
.cwm-card-name {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #334155;
    margin-bottom: 18px;
}
.cwm-card-value {
    font-size: 1.55rem;
    font-weight: 700;
    color: #F1F5F9;
    letter-spacing: -0.5px;
    margin-bottom: 3px;
}
.cwm-card-sub {
    font-size: 0.78rem;
    color: #475569;
    margin-bottom: 18px;
}
.cwm-card-sep {
    height: 1px;
    background: rgba(255,255,255,0.05);
    margin: 0 0 14px;
}
.cwm-card-pills {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
}
.cwm-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 6px;
    padding: 3px 9px;
    font-size: 0.7rem;
    color: #64748B;
    white-space: nowrap;
}
.cwm-pill b { color: #CBD5E1; font-weight: 600; }

/* ── Section title ──────────────────────────────────────────────────── */
.cwm-section {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2rem 0 1.1rem;
}
.cwm-section-icon {
    width: 34px; height: 34px;
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
    background: rgba(124,58,237,0.13);
}
.cwm-section-label {
    font-size: 0.95rem;
    font-weight: 700;
    color: #E2E8F0;
    letter-spacing: -0.2px;
    margin: 0;
}
.cwm-section-desc {
    font-size: 0.75rem;
    color: #475569;
    margin: 1px 0 0;
}

/* ── Currency block (Magazzino) ─────────────────────────────────────── */
.cwm-block {
    background: #0F0F1C;
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 14px;
    padding: 20px 20px 16px;
    margin-bottom: 14px;
}
.cwm-block-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
}
.cwm-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.cwm-block-value {
    font-size: 0.82rem;
    color: #475569;
    margin-left: auto;
}

/* ── Result receipt (Richiesta) ─────────────────────────────────────── */
.cwm-receipt {
    background: linear-gradient(135deg, #111120, #0E0E1A);
    border: 1px solid rgba(124,58,237,0.18);
    border-radius: 16px;
    padding: 24px;
    margin: 1rem 0;
}
.cwm-receipt-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.cwm-receipt-row:last-child { border-bottom: none; }
.cwm-receipt-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #475569;
}
.cwm-receipt-val {
    font-size: 1.15rem;
    font-weight: 700;
    color: #F1F5F9;
}
.cwm-receipt-val.ok   { color: #10B981; }
.cwm-receipt-val.warn { color: #F59E0B; }
.cwm-receipt-val.err  { color: #EF4444; }

/* ── Empty state ────────────────────────────────────────────────────── */
.cwm-empty {
    text-align: center;
    padding: 60px 20px;
    color: #334155;
}
.cwm-empty-icon { font-size: 3rem; margin-bottom: 12px; }
.cwm-empty-text { font-size: 0.9rem; font-weight: 500; }
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)
