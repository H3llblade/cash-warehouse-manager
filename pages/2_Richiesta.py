import streamlit as st
import pandas as pd
from datetime import datetime

from utils.storage import (
    load_warehouse,
    save_warehouse,
    load_history,
    save_history
)

from utils.constants import (
    CURRENCIES,
    CURRENCY_SYMBOLS
)

from utils.calculator import (
    calculate_withdrawal
)

st.title("💸 Nuova Richiesta")

warehouse = load_warehouse()

currency = st.selectbox(
    "Valuta",
    list(CURRENCIES.keys())
)

# Se l'utente cambia valuta, il risultato precedente non è più valido
if (
    "result" in st.session_state
    and st.session_state.get("result_currency") != currency
):
    del st.session_state["result"]

symbol = CURRENCY_SYMBOLS[currency]

# Valore minimo di una mazzetta per questa valuta (100 banconote × taglio minimo)
min_bundle_value = min(CURRENCIES[currency]) * 100

amount = st.number_input(
    f"Importo richiesto ({symbol})",
    min_value=0,
    step=min_bundle_value
)

if amount > 0 and amount < min_bundle_value:
    st.warning(
        f"Importo minimo prelevabile: {symbol}{min_bundle_value:,.0f} "
        f"(1 mazzetta da {min(CURRENCIES[currency])}{symbol} × 100 banconote)"
    )

if st.button("🧮 Calcola"):

    result = calculate_withdrawal(
        currency,
        amount,
        warehouse
    )

    st.session_state["result"] = result
    st.session_state["result_currency"] = currency

if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Richiesto",
        f"{symbol}{result['requested_amount']:,.0f}"
    )

    col2.metric(
        "Ottenuto",
        f"{symbol}{result['obtained_amount']:,.0f}"
    )

    col3.metric(
        "Differenza",
        f"{symbol}{result['difference']:,.0f}"
    )

    df = pd.DataFrame(result["details"])

    st.subheader("📦 Composizione Prelievo")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    if result["difference"] == 0:
        st.success("Importo ottenuto esattamente.")
    else:
        st.warning(
            f"Differenza di {symbol}{result['difference']:,.0f}"
        )

    if st.button("✅ Conferma Prelievo"):

        for item in result["details"]:
            tag = str(item["tag"])
            warehouse[currency][tag] -= item["notes_taken"]

        save_warehouse(warehouse)

        history = load_history()

        history.append({
            "timestamp":
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "currency":
                currency,
            "requested":
                result["requested_amount"],
            "obtained":
                result["obtained_amount"],
            "difference":
                result["difference"],
            "details":
                result["details"]
        })

        save_history(history)

        del st.session_state["result"]
        del st.session_state["result_currency"]

        st.success("Prelievo registrato.")
        st.rerun()
