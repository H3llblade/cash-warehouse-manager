import streamlit as st
from utils.storage import load_warehouse
from utils.constants import CURRENCIES, CURRENCY_SYMBOLS

st.markdown("""
<p class="cwm-page-title">💰 Dashboard</p>
<p class="cwm-page-sub">Monitoraggio in tempo reale del magazzino contante</p>
""", unsafe_allow_html=True)

warehouse = load_warehouse()

CARD_COLORS = {
    "EUR": ("#7C3AED", "#4F46E5"),
    "USD": ("#0891B2", "#0369A1"),
    "JPY": ("#DC2626", "#9F1239"),
    "GBP": ("#059669", "#065F46"),
}

# ── KPI cards ────────────────────────────────────────────────────────
cols = st.columns(4, gap="medium")

for i, (currency, tags) in enumerate(CURRENCIES.items()):
    symbol        = CURRENCY_SYMBOLS[currency]
    c1, c2        = CARD_COLORS[currency]
    total_bundles = 0
    total_value   = 0
    pills         = []

    for tag in tags:
        qty     = int(warehouse.get(currency, {}).get(str(tag), 0))
        bundles = qty // 100
        total_bundles += bundles
        total_value   += qty * tag
        pills.append(
            f'<div class="cwm-pill">{tag} → <b>{bundles}</b></div>'
        )

    with cols[i]:
        st.markdown(f"""
        <div class="cwm-card">
            <div class="cwm-card-bar"
                 style="background:linear-gradient(90deg,{c1},{c2});"></div>
            <div class="cwm-card-symbol"
                 style="background:linear-gradient(135deg,{c1},{c2});
                        -webkit-background-clip:text;
                        -webkit-text-fill-color:transparent;
                        background-clip:text;">{symbol}</div>
            <div class="cwm-card-name">{currency}</div>
            <div class="cwm-card-value">{symbol}{total_value:,.0f}</div>
            <div class="cwm-card-sub">{total_bundles} mazzette totali</div>
            <div class="cwm-card-sep"></div>
            <div class="cwm-card-pills">{"".join(pills)}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Dettaglio per taglio ─────────────────────────────────────────────
st.markdown("""
<div class="cwm-section">
    <div class="cwm-section-icon">📊</div>
    <div>
        <p class="cwm-section-label">Dettaglio per Taglio</p>
        <p class="cwm-section-desc">Scorte suddivise per denominazione</p>
    </div>
</div>
""", unsafe_allow_html=True)

for currency, tags in CURRENCIES.items():
    symbol = CURRENCY_SYMBOLS[currency]
    c1, _  = CARD_COLORS[currency]

    # Griglia fissa a 4 colonne — tutti i box hanno la stessa larghezza
    boxes_html = ""
    for tag in tags:
        qty     = int(warehouse.get(currency, {}).get(str(tag), 0))
        bundles = qty // 100
        boxes_html += f"""
        <div class="cwm-det-box">
            <div class="cwm-det-tag">{symbol}{tag}</div>
            <div class="cwm-det-val">{bundles} mazz.</div>
            <div class="cwm-det-notes">{qty:,} banconote</div>
        </div>"""

    # Celle vuote per riempire la griglia a 4
    for _ in range(4 - len(tags)):
        boxes_html += '<div class="cwm-det-box cwm-det-empty"></div>'

    st.markdown(f"""
    <div class="cwm-det-row">
        <div class="cwm-det-currency"
             style="color:{c1};">{currency}</div>
        <div class="cwm-det-grid">{boxes_html}</div>
    </div>
    """, unsafe_allow_html=True)
