import streamlit as st

st.set_page_config(
    page_title="Cash Warehouse Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema grafico
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1rem;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

[data-testid="stMetricValue"] {
    font-size: 24px;
    font-weight: bold;
}

.currency-card {
    padding: 15px;
    border-radius: 12px;
    background-color: #1f2937;
    text-align: center;
    border: 1px solid #374151;
}

.currency-title {
    font-size: 20px;
    font-weight: bold;
}

.currency-sub {
    font-size: 14px;
    color: #9ca3af;
}

</style>
""", unsafe_allow_html=True)

# Header
st.title("💰 Cash Warehouse Manager")

st.markdown(
    """
Sistema di gestione contanti multi-valuta con:

- 📦 Gestione Magazzino
- 💸 Richieste di Prelievo
- 📜 Storico Operazioni
- 🏦 Supporto EUR / USD / JPY / GBP
"""
)

st.divider()

# Dashboard rapida

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="currency-card">
        <div class="currency-title">EUR</div>
        <div class="currency-sub">
            100 / 50 / 20
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="currency-card">
        <div class="currency-title">USD</div>
        <div class="currency-sub">
            100 / 50 / 20 / 10
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="currency-card">
        <div class="currency-title">JPY</div>
        <div class="currency-sub">
            10000 / 5000 / 1000
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="currency-card">
        <div class="currency-title">GBP</div>
        <div class="currency-sub">
            50 / 20 / 10 / 5
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("🚀 Come utilizzare l'app")

st.markdown("""
### 1️⃣ Gestione Magazzino

Apri la pagina **Gestione Magazzino** dal menu laterale e inserisci il numero di banconote disponibili per ogni taglio.

---

### 2️⃣ Nuova Richiesta

Vai nella pagina **Nuova Richiesta** e inserisci:

- valuta
- importo richiesto

Premi:

```text
🧮 Calcola
