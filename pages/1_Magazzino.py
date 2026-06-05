import streamlit as st

from utils.storage import (
    load_warehouse,
    save_warehouse
)

from utils.constants import (
    CURRENCIES
)

st.title("📦 Gestione Magazzino")

warehouse = load_warehouse()

for currency, tags in CURRENCIES.items():

    st.subheader(currency)

    cols = st.columns(len(tags))

    warehouse.setdefault(currency, {})

    for i, tag in enumerate(tags):

        current_value = int(
            warehouse[currency].get(
                str(tag),
                0
            )
        )

        warehouse[currency][str(tag)] = cols[i].number_input(
            label=f"{tag}",
            min_value=0,
            value=current_value,
            step=100,
            key=f"warehouse_{currency}_{tag}"
        )

        bundles = (
            warehouse[currency][str(tag)]
            // 100
        )

        cols[i].caption(
            f"📦 {bundles} mazzette"
        )

    st.divider()

if st.button(
    "💾 Salva Magazzino",
    key="save_warehouse_button"
):

    save_warehouse(
        warehouse
    )

    st.success(
        "Magazzino salvato correttamente."
    )

st.divider()

st.subheader(
    "📊 Riepilogo Valore Magazzino"
)

for currency, tags in CURRENCIES.items():

    total_value = 0

    for tag in tags:

        total_value += (
            warehouse[currency].get(
                str(tag),
                0
            )
            * tag
        )

    st.metric(
        label=f"Totale {currency}",
        value=f"{total_value:,.0f}"
    )
