import streamlit as st
from utils.storage import load_warehouse
from utils.constants import CURRENCIES, CURRENCY_SYMBOLS

st.set_page_config(
    page_title="Cash Warehouse Manager",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Cash Warehouse Manager")

warehouse = load_warehouse()

cards = st.columns(4)

for i, (currency, tags) in enumerate(CURRENCIES.items()):

    symbol = CURRENCY_SYMBOLS[currency]
    total_bundles = 0
    total_value = 0

    for tag in tags:
        qty = int(warehouse.get(currency, {}).get(str(tag), 0))
        total_bundles += qty // 100
        total_value += qty * tag

    cards[i].markdown(
        f"""
        <div style="
            background:#1E1E1E;
            padding:20px;
            border-radius:15px;
            border:1px solid #333;
            text-align:center;
        ">
            <h1>{symbol}</h1>
            <h3>{total_bundles} mazzette</h3>
            <h4>{total_value:,.0f}</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

st.subheader("📦 Dettaglio Magazzino")

for currency, tags in CURRENCIES.items():

    symbol = CURRENCY_SYMBOLS[currency]
    st.markdown(f"## {symbol} {currency}")
    cols = st.columns(len(tags))

    for i, tag in enumerate(tags):
        qty = int(warehouse.get(currency, {}).get(str(tag), 0))
        cols[i].metric(
            label=str(tag),
            value=f"{qty // 100} mazz.",
            help=f"{qty:,} banconote totali"
        )
