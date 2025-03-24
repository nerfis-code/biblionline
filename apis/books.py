from Zlibrary import Zlibrary
import streamlit as st

from concurrent.futures import ThreadPoolExecutor

@st.cache_data(persist="disk")
def search(message,limit=10,page=0):
    Z = Zlibrary(email=st.secrets.zlibrary_account.email, password=st.secrets.zlibrary_account.password)
    results = Z.search(message=message,limit=limit,page=page)
    return results


async def parallel_search(messages: list[str], limit: int = 1, page: int = 0):
    Z = Zlibrary(email=st.secrets.zlibrary_account.email, password=st.secrets.zlibrary_account.password)
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(
            lambda q: Z.search(q, limit=3), 
            messages
        ))
    return results if results else [{"books":[]}]

    
def get_user_books():
    conn = st.connection('biblionline_db', type='sql')
    
    with conn.session as s:
        
        rented_books = \
            s.execute("SELECT * FROM rented_books WHERE user_id = :user_id", 
                                        {"user_id": st.session_state.user["id"]}
                                        ).mappings().fetchall()
        
        return rented_books