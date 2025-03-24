import streamlit as st
from apis.books import get_books_data, get_user_books
import components


components.nav()
if 'show_notification' not in st.session_state:
    st.session_state.show_notification = False
if 'notification_message' not in st.session_state:
    st.session_state.notification_message = ""


def show_rented_books():
    if not "collection" in st.session_state:
        st.session_state.collection= get_user_books() 
    rented_books = get_books_data(st.session_state.collection)

    if rented_books:
        st.title("Mis Libros Prestados")
        col1, col2, col3 = st.columns(3)
        cols = [col1,col2,col3]
        col_index = 0
        for book in rented_books:
            with cols[col_index]:
                container = st.container(border=True)
                container.write(f"**Título:** {book['title']}")
                container.image(book['cover'])
                container.link_button(label="Leer online",url=book["readOnlineUrl"])
                    
                if container.button(f"Devolver {book['title']}", key=f"return_{book['title']}"):  
                    success = return_book(book['md5'], st.session_state.user["id"])
                    if success:
                        st.session_state.notification_message = f"Libro '{book['title']}' devuelto correctamente."
                        st.session_state.show_notification = True

                        st.rerun()  # Usando st.rerun() en lugar de experimental_rerun
                        if "notification" in st.session_state:
                            st.success(st.session_state.notification)
                            del st.session_state.notification  
                col_index =(col_index+1)%len(cols)
        
    else:
        st.info("No tienes libros prestados en este momento.")

    
def return_book(book_md5, user_id):
    try:
        conn = st.connection('biblionline_db', type='sql')
        with conn.session as s:
            
            s.execute("DELETE FROM rented_books WHERE user_id = :user_id AND book_md5 = :book_md5", 
                      {
                        'user_id': user_id,
                        'book_md5': book_md5
                        })
            s.commit()
        st.session_state.collection= get_user_books() 
        return True
    except Exception as e:
        st.error(f"Error al devolver el libro: {e}")
        return False
@st.dialog("Libro")
def show_notification():
    if st.session_state.show_notification:
        st.html("<p style='color:green'>Se a regresado el lirbo son exito</p>")
        if st.button("Cerrar", key="close_notification"):
            st.session_state.show_notification = False
            st.rerun()


if "user" in st.session_state and st.session_state.user:
    show_rented_books()
else:
    st.info("Para poder ver tu coleccion de libros debes iniciar sesion")

    st.page_link(label="Inicia Sesion",page="pages/1_login.py", icon="👤")

if st.session_state.show_notification:
    show_notification()