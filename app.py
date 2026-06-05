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

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.info("EUR\n\n100 / 50 / 20")

    with col2:
        st.info("USD\n\n100 / 50 / 20 / 10")

    with col3:
        st.info("JPY\n\n10000 / 5000 / 1000")

    with col4:
        st.info("GBP\n\n50 / 20 / 10 / 5")

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
