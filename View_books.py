import streamlit as st
from apis import books
from datetime import datetime, timedelta
import components
from apis.books import get_user_books

st.set_page_config(
    page_title="Vista de libros",
    page_icon="📚"
)
components.nav()

userExist = "user" in st.session_state and st.session_state.user


if not "response" in st.session_state:
    st.session_state.response = {"page":1, "books":[], "message":"batman"}
    
@st.dialog("Libro",width="large")
def view_book(res):
    col1, col2 = st.columns(2)
    with col1:
        st.title(res["title"])
        st.image(res["cover"])
        if userExist:
            if not "collection" in st.session_state:
                st.session_state.collection= get_user_books() 
            if st.button("Rentar",use_container_width=True):
                
                if not res["md5"] in st.session_state.collection:
                    now = datetime.now()
                    end_date = now + timedelta(days=30)
                    end_date = end_date.strftime("%m/%d/%Y, %H:%M:%S")
                
                    conn = st.connection('biblionline_db', type='sql')
                    with conn.session as s:
                        s.execute("""
                                    INSERT INTO rented_books (user_id, book_md5, rent_date) 
                                    VALUES (:user_id, :book_md5, :rent_date)
                                    """, {
                                        'user_id': st.session_state.user["id"], 
                                        'book_md5': res["md5"], 
                                        'rent_date': end_date})
                        s.commit()
                    st.session_state.collection.append(res["md5"])
                else:
                    with col2:
                        st.info("Ya tienes rentado este libro")      
        else:
            st.button("Rentar",use_container_width=True,disabled=True,help="Necesitas iniciar sesion")    
        
    with col2:
        if len(res["description"]) != 0:
            st.title("Descripcion")
            st.markdown(res["description"],unsafe_allow_html=True)   
        else:
            st.caption("No posee description")
        
#st.title("Estoy viendo los libros")

col1, col2, col3 = st.columns([1,2,1])  # Columnas con proporciones
with col2:
    st.image("image/biblionline_logo.png", width=300)  # Ajusta el ancho según necesites


st.markdown("## 📚 Explora nuestra colección de libros")
text_search = st.text_input("Deja que tu imaginacion vuele", value="")

if text_search and st.session_state.response["message"] != text_search:
    st.session_state.response["message"] = text_search
    st.session_state.response["page"] = 0
    st.session_state.response["books"]= []
    
if len(st.session_state.response["books"]) == 0:
    res_books = books.search(st.session_state.response["message"])
    if res_books:
        st.session_state.response["books"] = res_books["books"]
    else:
        st.info("Hubo un error en la busque de libros")
    

    
col1, col2, col3, col4 = st.columns(4)
cols = [col1,col2,col3,col4,]

colIndex = 0

for res in st.session_state.response["books"]:
    with cols[colIndex]:
        container = st.container(border=True)
        if res["cover"] != "/img/cover-not-exists.png":
            container.image(res["cover"])
        else:
            container.text(res["title"])
        if container.button("ver", key=res["md5"]): 
            view_book(res)
            
    colIndex += 1
    colIndex %= len(cols)

if st.button("Seguir buscando",use_container_width=True):
    st.session_state.response["page"] += 1
    res_books = books.search(st.session_state.response["message"],page=st.session_state.response["page"])
    if res_books:
        for book in res_books["books"]:
            if not book in st.session_state.response["books"]:
                st.session_state.response["books"].append(book)
        st.rerun()
        
    else:
        st.info("hubo un error en la busqueda de libros")
    
