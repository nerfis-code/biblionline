# pages/page_rented_books.py
import streamlit as st
from sqlalchemy import text



# Configurar estado para la notificación
if 'show_notification' not in st.session_state:
    st.session_state.show_notification = False
if 'notification_message' not in st.session_state:
    st.session_state.notification_message = ""

# Función para mostrar libros prestados
def show_rented_books():
    # Conectar a la base de datos
    conn = st.connection('biblionline_db', type='sql')
    
    # Consulta SQL para obtener los libros prestados por el usuario actual
    query = text("""
        SELECT * FROM rented_books 
        WHERE user_id = :user_id
    """)
    
    # Ejecutar la consulta con parámetros y obtener resultados como diccionarios
    rented_books = conn.session.execute(query, {"user_id": st.session_state.user["id"]}).mappings().fetchall()
    
    if rented_books:
        st.title("Mis Libros Prestados")
        for book in rented_books:
            with st.container(border=True):
                st.write(f"**Título:** {book['book_title']}")
                if st.button(f"Devolver {book['book_title']}", key=f"return_{book['book_title']}"):
                    # Llamar directamente a la función de devolución sin usar el diálogo
                    success = return_book(book['book_title'], st.session_state.user["id"])
                    if success:
                        st.session_state.notification_message = f"Libro '{book['book_title']}' devuelto correctamente."
                        st.session_state.show_notification = True

                        st.rerun()  # Usando st.rerun() en lugar de experimental_rerun
                        if "notification" in st.session_state:
                         st.success(st.session_state.notification)
                        del st.session_state.notification  
        
    else:
        st.info("No tienes libros prestados en este momento.")

# Función para devolver un libro 
def return_book(book_title, user_id):
    try:
        conn = st.connection('biblionline_db', type='sql')
        with conn.session as s:
            # Consulta SQL para eliminar el libro prestado
            query = text("""
                DELETE FROM rented_books 
                WHERE user_id = :user_id AND book_title = :book_title
            """)
            s.execute(query, {
                'user_id': user_id,
                'book_title': book_title
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