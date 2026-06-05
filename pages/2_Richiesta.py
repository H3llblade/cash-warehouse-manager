import streamlit as st
import pandas as pd

from utils.constants import (
    CURRENCIES,
    CURRENCY_SYMBOLS
)

from utils.storage import (
    load_warehouse
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

symbol = CURRENCY_SYMBOLS[currency]

amount = st.number_input(
    f"Importo richiesto ({symbol})",
    min_value=0,
    step=1000
)

if st.button("🧮 Calcola"):

    result = calculate_withdrawal(
        currency,
        amount,
        warehouse
    )

    st.subheader("Riepilogo")

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

    rows = []

    for item in result["details"]:

        rows.append(
            {
                "Taglio":
                    item["tag"],

                "Banconote da prendere":
                    item["notes_taken"],

                "Mazzette":
                    item["bundles_taken"],

                "Valore":
                    item["value_taken"],

                "Banconote residue":
                    item["remaining_notes"],

                "Mazzette residue":
                    item["remaining_bundles"]
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True
    )

    st.session_state[
        "last_calculation"
    ] = result
