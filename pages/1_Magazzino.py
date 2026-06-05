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

        current_value = warehouse[currency].get(
            str(tag),
            0
        )

        warehouse[currency][str(tag)] = cols[i].number_input(
            f"{tag}",
            min_value=0,
            value=current_value,
            step=100
        )

        bundles = warehouse[currency][str(tag)] // 100

        cols[i].caption(
            f"📦 {bundles} mazzette"
        )

st.divider()

if st.button("💾 Salva Magazzino"):

    save_warehouse(warehouse)

    st.success(
        "Magazzino salvato correttamente."
    )
