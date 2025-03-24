import streamlit as st
from sqlalchemy import text
from apis import books
from datetime import datetime, timedelta
import sqlite3

@st.dialog("Libro",width="large")
def view_book(res):
    col1, col2 = st.columns(2)
    with col1:
        st.title(res["title"])
        st.image(res["cover"])
        if st.button("Rentar",use_container_width=True):
            # st.session_state.vote = {"item": item, "reason": reason}
            
            #peticion
            now = datetime.now()
         
            end_date = now + timedelta(days=30)
            end_date = end_date.strftime("%m/%d/%Y, %H:%M:%S")
           
            conn = st.connection('biblionline_db', type='sql')
            with conn.session as s:
                s.execute(text("""
                               INSERT INTO rented_books (user_id, book_title, rent_date) 
                               VALUES (:user_id, :book_title, :rent_date)
                            """), {
                                'user_id': st.session_state.user["id"], 
                                'book_title': res["title"], 
                                'rent_date': end_date})
                          
                
                s.commit()

                
            
        
    with col2:
        st.title("Descripcion")
        st.markdown(res["description"],unsafe_allow_html=True)


    
        
st.title("Estoy viendo los libros")
text_search = st.text_input("Search videos by title or speaker", value="")
if text_search:
    response = books.search(text_search)["books"]
else:
    response = books.search("batman")["books"]  
    
col1, col2, col3, col4 = st.columns(4)
cols = [col1,col2,col3,col4,]

st.code(response,wrap_lines=True)

colIndex = 0
for res in response:
    with cols[colIndex]:
        container = st.container(border=True)
        container.image(res["cover"])
        if container.button("Rentar", key=res["id"]): 
            view_book(res)
    colIndex += 1
    colIndex %= len(cols)

