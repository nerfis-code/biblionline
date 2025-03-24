from Zlibrary import Zlibrary
import streamlit as st
import asyncio
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
    
    @st.cache_data(persist="disk")
    def get_book_info(book_list):
        print("####",book_list)
        md5_list = list(map(lambda b : b["book_md5"],book_list))
        res = []
        for info in asyncio.run(parallel_search(md5_list)):
            if info:
                res.append(info["books"][0])
            
        return res
        
    with conn.session as s:
        
        rented_books = \
            s.execute("SELECT * FROM rented_books WHERE user_id = :user_id", 
                                        {"user_id": st.session_state.user["id"]}
                                        ).mappings().fetchall()
        
        res = get_book_info([dict(row) for row in rented_books])
        return list(res)