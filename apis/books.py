from Zlibrary import Zlibrary
import streamlit as st

cache = {}
@st.cache_data(persist="disk")
def search(message,limit=10,page=0):

    Z = Zlibrary(email=st.secrets.zlibrary_account.email, password=st.secrets.zlibrary_account.password)
    results = Z.search(message=message,limit=limit,page=page)
    return results if results else {"books":[]}

def get_user_books():
    conn = st.connection('biblionline_db', type='sql')
    
    with conn.session as s:
        
        rented_books = \
            s.execute("SELECT * FROM rented_books WHERE user_id = :user_id", 
                                        {"user_id": st.session_state.user["id"]}
                                        ).mappings().fetchall()
        
        return rented_books