import streamlit as st
import pandas as pd

from utils.storage import load_history
from utils.constants import CURRENCY_SYMBOLS

st.markdown("""
<p class="cwm-page-title">📜 Storico Operazioni</p>
<p class="cwm-page-sub">Cronologia completa di tutti i prelievi effettuati</p>
""", unsafe_allow_html=True)

history = load_history()

if not history:
    st.markdown("""
    <div class="cwm-empty">
        <div class="cwm-empty-icon">🗂️</div>
        <div class="cwm-empty-text">Nessuna operazione registrata</div>
    </div>
    """, unsafe_allow_html=True)

else:
    BADGE_COLORS = {
        "EUR": ("rgba(124,58,237,0.15)", "#A78BFA"),
        "USD": ("rgba(8,145,178,0.15)",  "#67E8F9"),
        "JPY": ("rgba(220,38,38,0.15)",  "#FCA5A5"),
        "GBP": ("rgba(5,150,105,0.15)",  "#6EE7B7"),
    }

    # ── Tabella riepilogativa ────────────────────────────────────────
    st.markdown("""
    <div class="cwm-section">
        <div class="cwm-section-icon">📋</div>
        <div>
            <p class="cwm-section-label">Riepilogo</p>
            <p class="cwm-section-desc">Tutte le operazioni in ordine cronologico</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    rows = []
    for op in history:
        sym  = CURRENCY_SYMBOLS.get(op["currency"], "")
        diff = op.get("difference", op["obtained"] - op["requested"])
        rows.append({
            "Data":       op.get("timestamp", "-"),
            "Valuta":     op["currency"],
            "Richiesto":  f"{sym}{op['requested']:,.0f}",
            "Ottenuto":   f"{sym}{op['obtained']:,.0f}",
            "Differenza": f"{'+' if diff > 0 else ''}{sym}{diff:,.0f}",
        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )

    # ── Dettaglio operazioni ─────────────────────────────────────────
    st.markdown("""
    <div class="cwm-section">
        <div class="cwm-section-icon">🔍</div>
        <div>
            <p class="cwm-section-label">Dettaglio operazioni</p>
            <p class="cwm-section-desc">Clicca su un'operazione per espandere il dettaglio</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for op in reversed(history):
        sym       = CURRENCY_SYMBOLS.get(op["currency"], "")
        bg, fg    = BADGE_COLORS.get(op["currency"], ("rgba(255,255,255,0.06)", "#94A3B8"))
        diff      = op.get("difference", op["obtained"] - op["requested"])
        diff_sign = "+" if diff > 0 else ""

        label = (
            f"{op.get('timestamp', '-')}  ·  "
            f"{op['currency']}  ·  "
            f"{sym}{op['requested']:,.0f} richiesti  →  "
            f"{sym}{op['obtained']:,.0f} ottenuti"
        )

        with st.expander(label):
            d_cols = st.columns(3)
            d_cols[0].metric("Richiesto",  f"{sym}{op['requested']:,.0f}")
            d_cols[1].metric("Ottenuto",   f"{sym}{op['obtained']:,.0f}")
            d_cols[2].metric("Differenza", f"{diff_sign}{sym}{diff:,.0f}")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            detail_df = pd.DataFrame(op["details"]).rename(columns={
                "tag":               "Taglio",
                "bundles_taken":     "Mazzette",
                "notes_taken":       "Banconote",
                "value_taken":       "Valore",
                "remaining_notes":   "Banconote Residue",
                "remaining_bundles": "Mazzette Residue",
            })

            st.dataframe(detail_df, use_container_width=True, hide_index=True)
