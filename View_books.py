import streamlit as st
from sqlalchemy import text
from apis import books
from datetime import datetime, timedelta
import sqlite3
from PIL import Image


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
                               INSERT INTO rented_books (user_id, book_md5, rent_date) 
                               VALUES (:user_id, :book_md5, :rent_date)
                            """), {
                                'user_id': st.session_state.user["id"], 
                                'book_md5': res["md5"], 
                                'rent_date': end_date})
                s.commit()       
        
    with col2:
        st.title("Descripcion")
        st.markdown(res["description"],unsafe_allow_html=True)   
        
#st.title("Estoy viendo los libros")
img = Image.open("image/biblionline_logo.png")
col1, col2, col3 = st.columns([1,2,1])  # Columnas con proporciones
with col2:
    st.image(img, width=300)  # Ajusta el ancho según necesites


st.markdown("## 📚 Explora nuestra colección de libros")
text_search = st.text_input("Deja que tu imaginacion vuele", value="")
response = books.search(text_search if text_search else "batman")

if not response:
    res_books = []
    st.error("No se encuentra libros")
else:
    res_books = response["books"]
    
col1, col2, col3, col4 = st.columns(4)
cols = [col1,col2,col3,col4,]

st.code(res_books,wrap_lines=True)

colIndex = 0
for res in res_books:
    with cols[colIndex]:
        container = st.container(border=True)
        container.image(res["cover"])
        if container.button("Rentar", key=res["id"]): 
            view_book(res)
    colIndex += 1
    colIndex %= len(cols)

