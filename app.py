import streamlit as st
from utils.styles import inject_css

st.set_page_config(
    page_title="Cash Warehouse Manager",
    page_icon="💰",
    layout="wide"
)

inject_css()

pg = st.navigation([
    st.Page("views/dashboard.py",    title="Dashboard",  icon="💰"),
    st.Page("pages/1_Magazzino.py",  title="Magazzino",  icon="📦"),
    st.Page("pages/2_Richiesta.py",  title="Richiesta",  icon="💸"),
    st.Page("pages/3_Storico.py",    title="Storico",    icon="📜"),
])

pg.run()
