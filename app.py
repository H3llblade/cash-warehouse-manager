import streamlit as st
import json
import os

st.set_page_config(
    page_title="Cash Warehouse Manager",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# FILES
# -----------------------------

WAREHOUSE_FILE = "warehouse.json"
HISTORY_FILE = "history.json"

# -----------------------------
# UTILS
# -----------------------------

def load_warehouse():
    if not os.path.exists(WAREHOUSE_FILE):
        return {
            "EUR":{"100":0,"50":0,"20":0},
            "USD":{"100":0,"50":0,"20":0,"10":0},
            "JPY":{"10000":0,"5000":0,"1000":0},
            "GBP":{"50":0,"20":0,"10":0,"5":0}
        }

    with open(WAREHOUSE_FILE,"r") as f:
        return json.load(f)

def save_warehouse(data):
    with open(WAREHOUSE_FILE,"w") as f:
        json.dump(data,f,indent=4)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE,"r") as f:
        return json.load(f)

def save_history(data):
    with open(HISTORY_FILE,"w") as f:
        json.dump(data,f,indent=4)

# -----------------------------
# VALUTE
# -----------------------------

currencies = {
    "EUR": [100, 50, 20],
    "USD": [100, 50, 20, 10],
    "JPY": [10000, 5000, 1000],
    "GBP": [50, 20, 10, 5]
}

currency_symbols = {
    "EUR": "€",
    "USD": "$",
    "JPY": "¥",
    "GBP": "£"
}

# -----------------------------
# MENU
# -----------------------------

page = st.sidebar.radio(
    "Navigazione",
    [
        "Dashboard",
        "Magazzino",
        "Richiesta",
        "Storico"
    ]
)

# -----------------------------
# DASHBOARD
# -----------------------------

if page == "Dashboard":

    st.title("💰 Cash Warehouse Manager")

    warehouse = load_warehouse()

    st.subheader("📊 Situazione Magazzino")

    col1, col2, col3, col4 = st.columns(4)

    cards = [
        ("EUR", "€", col1),
        ("USD", "$", col2),
        ("JPY", "¥", col3),
        ("GBP", "£", col4)
    ]

    for currency, symbol, col in cards:

        total_notes = 0
        total_bundles = 0
        total_value = 0

        for tag, qty in warehouse[currency].items():

            qty = int(qty)

            total_notes += qty
            total_bundles += qty // 100
            total_value += qty * int(tag)

        col.metric(
            label=f"{symbol} Mazzette",
            value=total_bundles
        )

        col.metric(
            label=f"{symbol} Valore",
            value=f"{total_value:,.0f}"
        )

    st.divider()

    st.subheader("Dettaglio Tagli")

    for currency, symbol, _ in cards:

        st.markdown(f"### {symbol}")

        cols = st.columns(len(warehouse[currency]))

        for i, (tag, qty) in enumerate(
            warehouse[currency].items()
        ):

            cols[i].metric(
                label=f"{tag}",
                value=f"{qty // 100} mazz."
            )

# -----------------------------
# MAGAZZINO
# -----------------------------

elif page == "Magazzino":

    st.title("📦 Magazzino")

    warehouse = load_warehouse()

    currencies = {
        "EUR": [100, 50, 20],
        "USD": [100, 50, 20, 10],
        "JPY": [10000, 5000, 1000],
        "GBP": [50, 20, 10, 5]
    }

    for currency, tags in currencies.items():

        st.subheader(currency)

        cols = st.columns(len(tags))

        for i, tag in enumerate(tags):

            current = int(
                warehouse[currency].get(
                    str(tag),
                    0
                )
            )

            warehouse[currency][str(tag)] = cols[i].number_input(
                label=f"{currency}-{tag}",
                value=current,
                min_value=0,
                step=100,
                key=f"{currency}_{tag}"
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
        "💾 Salva",
        key="save_warehouse"
    ):

        save_warehouse(
            warehouse
        )

        st.success(
            "Magazzino aggiornato"
        )

# -----------------------------
# RICHIESTA
# -----------------------------

elif page == "Richiesta":

    st.title("💸 Nuova Richiesta")

    warehouse = load_warehouse()

    currency = st.selectbox(
        "Valuta",
        ["EUR","USD","JPY","GBP"]
    )

    amount = st.number_input(
        "Importo richiesto",
        min_value=0
    )

    st.warning(
        "La logica avanzata verrà collegata qui."
    )

# -----------------------------
# STORICO
# -----------------------------

elif page == "Storico":

    st.title("📜 Storico")

    history = load_history()

    if not history:

        st.info(
            "Nessuna operazione registrata."
        )

    else:

        st.json(history)
