import streamlit as st
import pandas as pd

from utils.storage import (
    load_history
)

st.title(
    "📜 Storico Operazioni"
)

history = load_history()

if not history:

    st.info(
        "Nessuna operazione registrata."
    )

else:

    rows = []

    for operation in history:

        rows.append(
            {
                "Data":
                    operation[
                        "timestamp"
                    ],

                "Valuta":
                    operation[
                        "currency"
                    ],

                "Richiesto":
                    operation[
                        "requested"
                    ],

                "Ottenuto":
                    operation[
                        "obtained"
                    ]
            }
        )

    df = pd.DataFrame(
        rows
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Dettaglio Operazioni"
    )

    for operation in reversed(
        history
    ):

        with st.expander(
            f"{operation['timestamp']} - {operation['currency']}"
        ):

            st.json(
                operation
            )
