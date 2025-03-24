
import streamlit as st

from apis.books import get_user_books




if 'show_notification' not in st.session_state:
    st.session_state.show_notification = False
if 'notification_message' not in st.session_state:
    st.session_state.notification_message = ""


def show_rented_books():

    rented_books = get_user_books()

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
        
    else:
        st.info("No tienes libros prestados en este momento.")
    st.text(rented_books)
# Función para devolver un libro 
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
        return True
    except Exception as e:
        st.error(f"Error al devolver el libro: {e}")
        return False

def show_notification():
    if st.session_state.show_notification:
        # Usar columns para centrar el contenido
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Contenedor de notificación con estilo
            st.markdown(
                f"""
                <div style='
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                    text-align: center;
                    margin: 20px 0;
                '>
                    <h3>✅ {st.session_state.notification_message}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button("Cerrar", key="close_notification"):
                st.session_state.show_notification = False
                st.rerun()


# Mostrar la página de libros prestados
show_rented_books()


if st.session_state.show_notification:
    show_notification()