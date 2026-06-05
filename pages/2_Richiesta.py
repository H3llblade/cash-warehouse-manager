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

st.title(
    "💸 Nuova Richiesta"
)

warehouse = load_warehouse()

currency = st.selectbox(
    "Valuta",
    list(
        CURRENCIES.keys()
    )
)

symbol = (
    CURRENCY_SYMBOLS[currency]
)

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

    st.session_state[
        "result"
    ] = result

if "result" in st.session_state:

    result = (
        st.session_state["result"]
    )

    st.subheader(
        "Risultato"
    )

    st.metric(
        "Totale ottenuto",
        f"{symbol}{result['obtained_amount']:,.0f}"
    )

    st.metric(
        "Differenza",
        f"{symbol}{result['difference']:,.0f}"
    )

    df = pd.DataFrame(
        result["details"]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    if st.button(
        "✅ Conferma Prelievo"
    ):

        for item in result["details"]:

            tag = str(
                item["tag"]
            )

            warehouse[currency][tag] -= (
                item["notes_taken"]
            )

        save_warehouse(
            warehouse
        )

        history = (
            load_history()
        )

        history.append(
            {
                "timestamp":
                    datetime.now()
                    .strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),

                "currency":
                    currency,

                "requested":
                    result[
                        "requested_amount"
                    ],

                "obtained":
                    result[
                        "obtained_amount"
                    ],

                "details":
                    result[
                        "details"
                    ]
            }
        )

        save_history(
            history
        )

        st.success(
            "Prelievo registrato."
        )

        del st.session_state[
            "result"
        ]

        st.rerun()
