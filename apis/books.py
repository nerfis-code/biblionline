from Zlibrary import Zlibrary
import streamlit as st

cache = {}
@st.cache_data
def search(message,limit=5):
    if message in cache:
        return cache[message]
    # Create Zlibrary object and login
    Z = Zlibrary(email=st.secrets.zlibrary_account.email, password=st.secrets.zlibrary_account.password)

    # Search for books
    results = Z.search(message=message,limit=limit)
    cache[message] = results
    
    return results if results else {"books":[]}