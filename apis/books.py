from Zlibrary import Zlibrary
import streamlit as st

cache = {}
def search(message):
    if message in cache:
        return cache[message]
    # Create Zlibrary object and login
    Z = Zlibrary(email=st.secrets.zlibrary_account.email, password=st.secrets.zlibrary_account.password)

    # Search for books
    results = Z.search(message=message,limit=5)
    cache[message] = results
    
    return results if results else {"books":[]}