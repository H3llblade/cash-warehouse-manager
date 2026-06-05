import streamlit as st
from utils.storage import load_warehouse, save_warehouse
from utils.constants import CURRENCIES, CURRENCY_SYMBOLS

st.markdown("""
<p class="cwm-page-title">📦 Gestione Magazzino</p>
<p class="cwm-page-sub">Modifica le scorte di banconote per ciascuna valuta</p>
""", unsafe_allow_html=True)

warehouse = load_warehouse()

BADGE_COLORS = {
    "EUR": ("rgba(124,58,237,0.15)", "#A78BFA"),
    "USD": ("rgba(8,145,178,0.15)",  "#67E8F9"),
    "JPY": ("rgba(220,38,38,0.15)",  "#FCA5A5"),
    "GBP": ("rgba(5,150,105,0.15)",  "#6EE7B7"),
}

for currency, tags in CURRENCIES.items():
    symbol       = CURRENCY_SYMBOLS[currency]
    bg, fg       = BADGE_COLORS[currency]

    warehouse.setdefault(currency, {})

    total_value = sum(
        int(warehouse[currency].get(str(t), 0)) * t
        for t in tags
    )

    st.markdown(f"""
    <div class="cwm-block">
        <div class="cwm-block-head">
            <span class="cwm-badge"
                  style="background:{bg}; color:{fg};">{currency}</span>
            <span style="font-size:1.3rem;">{symbol}</span>
            <span class="cwm-block-value">
                Valore totale: <b style="color:#CBD5E1;">{symbol}{total_value:,.0f}</b>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(tags), gap="medium")

    for i, tag in enumerate(tags):
        current = int(warehouse[currency].get(str(tag), 0))
        with cols[i]:
            new_val = st.number_input(
                label=f"{symbol}{tag}",
                min_value=0,
                value=current,
                step=100,
                key=f"wh_{currency}_{tag}"
            )
            warehouse[currency][str(tag)] = int(new_val)

            bundles = int(new_val) // 100
            st.markdown(
                f"<div style='text-align:center; margin-top:4px;'>"
                f"<span style='font-size:0.72rem; font-weight:600; "
                f"color:{fg}; background:{bg}; padding:2px 8px; "
                f"border-radius:5px;'>📦 {bundles} mazz.</span></div>",
                unsafe_allow_html=True
            )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

col_btn, col_msg = st.columns([1, 3])

with col_btn:
    if st.button("💾 Salva Magazzino", key="save_btn", use_container_width=True):
        save_warehouse(warehouse)
        col_msg.success("Magazzino salvato correttamente.")
