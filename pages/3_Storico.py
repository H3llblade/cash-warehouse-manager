import streamlit as st
import pandas as pd

from utils.storage import load_history

st.title("📜 Storico Operazioni")

history = load_history()

if not history:

    st.info("Nessuna operazione registrata.")

else:

    rows = []

    for op in history:
        rows.append({
            "Data":       op.get("timestamp", "-"),
            "Valuta":     op["currency"],
            "Richiesto":  op["requested"],
            "Ottenuto":   op["obtained"],
            "Differenza": op.get("difference", op["obtained"] - op["requested"])
        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Dettaglio Operazioni")

    for op in reversed(history):

        with st.expander(
            f"{op.get('timestamp', '-')} — {op['currency']} — richiesto: {op['requested']:,.0f}"
        ):
            st.dataframe(
                pd.DataFrame(op["details"]),
                use_container_width=True,
                hide_index=True
            )
