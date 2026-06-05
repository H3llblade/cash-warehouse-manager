import streamlit as st
from streamlit_local_storage import LocalStorage

_DEFAULT_WAREHOUSE = {
    "EUR": {"100": 0, "50": 0, "20": 0},
    "USD": {"100": 0, "50": 0, "20": 0, "10": 0},
    "JPY": {"10000": 0, "5000": 0, "1000": 0},
    "GBP": {"50": 0, "20": 0, "10": 0, "5": 0}
}


def _storage():
    return LocalStorage()


def load_warehouse():
    data = _storage().getItem("warehouse")
    if not data:
        return {
            k: dict(v)
            for k, v in _DEFAULT_WAREHOUSE.items()
        }
    return data


def save_warehouse(data):
    _storage().setItem("warehouse", data)


def load_history():
    data = _storage().getItem("history")
    if not data:
        return []
    return data


def save_history(data):
    _storage().setItem("history", data)


def add_history_entry(entry):
    history = load_history()
    history.append(entry)
    save_history(history)
