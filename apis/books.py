from Zlibrary import Zlibrary
import streamlit as st

def search(message):
    # Create Zlibrary object and login
    Z = Zlibrary(email=st.secrets.zlibrary_account.email, password=st.secrets.zlibrary_account.password)

    # Search for books
    results = Z.search(message=message)

    return results