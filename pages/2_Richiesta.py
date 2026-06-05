import streamlit as st
import pandas as pd
from datetime import datetime

from utils.storage import load_warehouse, save_warehouse, load_history, save_history
from utils.constants import CURRENCIES, CURRENCY_SYMBOLS
from utils.calculator import calculate_withdrawal

st.markdown("""
<p class="cwm-page-title">💸 Nuova Richiesta</p>
<p class="cwm-page-sub">Calcola la composizione ottimale del prelievo per mazzette</p>
""", unsafe_allow_html=True)

warehouse = load_warehouse()

col_form, col_space = st.columns([1, 2])

with col_form:
    currency = st.selectbox("Valuta", list(CURRENCIES.keys()))

    if (
        "result" in st.session_state
        and st.session_state.get("result_currency") != currency
    ):
        del st.session_state["result"]

    symbol          = CURRENCY_SYMBOLS[currency]
    min_bundle_val  = min(CURRENCIES[currency]) * 100

    amount = st.number_input(
        f"Importo richiesto ({symbol})",
        min_value=0,
        step=min_bundle_val
    )

    if amount > 0 and amount < min_bundle_val:
        st.warning(
            f"Minimo prelevabile: {symbol}{min_bundle_val:,.0f} "
            f"(1 mazzetta × {min(CURRENCIES[currency])}{symbol})"
        )

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    if st.button("🧮 Calcola", use_container_width=True):
        result = calculate_withdrawal(currency, amount, warehouse)
        st.session_state["result"]          = result
        st.session_state["result_currency"] = currency

# ── Risultato ────────────────────────────────────────────────────────
if "result" in st.session_state:

    result  = st.session_state["result"]
    diff    = result["difference"]

    diff_class = "ok" if diff == 0 else ("warn" if diff > 0 else "err")
    diff_sign  = "+" if diff > 0 else ""

    st.markdown(f"""
    <div class="cwm-section">
        <div class="cwm-section-icon">🧾</div>
        <div>
            <p class="cwm-section-label">Riepilogo Prelievo</p>
            <p class="cwm-section-desc">{currency} — importo richiesto {symbol}{result['requested_amount']:,.0f}</p>
        </div>
    </div>

    <div class="cwm-receipt">
        <div class="cwm-receipt-row">
            <span class="cwm-receipt-label">Importo richiesto</span>
            <span class="cwm-receipt-val">{symbol}{result['requested_amount']:,.0f}</span>
        </div>
        <div class="cwm-receipt-row">
            <span class="cwm-receipt-label">Importo ottenuto</span>
            <span class="cwm-receipt-val">{symbol}{result['obtained_amount']:,.0f}</span>
        </div>
        <div class="cwm-receipt-row">
            <span class="cwm-receipt-label">Differenza</span>
            <span class="cwm-receipt-val {diff_class}">{diff_sign}{symbol}{diff:,.0f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabella composizione
    st.markdown("""
    <div class="cwm-section">
        <div class="cwm-section-icon">📦</div>
        <div>
            <p class="cwm-section-label">Composizione per taglio</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame(result["details"]).rename(columns={
        "tag":               "Taglio",
        "bundles_taken":     "Mazzette",
        "notes_taken":       "Banconote",
        "value_taken":       "Valore",
        "remaining_notes":   "Banconote Residue",
        "remaining_bundles": "Mazzette Residue",
    })

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    col_btn, col_msg = st.columns([1, 3])

    with col_btn:
        if st.button("✅ Conferma Prelievo", use_container_width=True):

            for item in result["details"]:
                warehouse[currency][str(item["tag"])] -= item["notes_taken"]

            save_warehouse(warehouse)

            history = load_history()
            history.append({
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "currency":  currency,
                "requested": result["requested_amount"],
                "obtained":  result["obtained_amount"],
                "difference": result["difference"],
                "details":   result["details"],
            })
            save_history(history)

            del st.session_state["result"]
            del st.session_state["result_currency"]

            col_msg.success("Prelievo confermato e registrato nello storico.")
            st.rerun()
