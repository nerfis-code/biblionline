# pages/page_rented_books.py
import streamlit as st
from sqlalchemy import text

# Función para mostrar libros prestados
def show_rented_books():
    # Conectar a la base de datos
    conn = st.connection('biblionline_db', type='sql')

    # Consulta SQL para obtener los libros prestados por el usuario actual
    query = text("""
        SELECT book_title FROM rented_books 
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
                    return_book({"title": book["book_title"], "cover": "", "description": ""})
    else:
        st.info("No tienes libros prestados en este momento.")

# Función para devolver un libro
@st.dialog("Devolver Libro", width="large")
def return_book(res):
    st.title(f"Devolver Libro: {res['title']}")
    st.image(res["cover"])
    st.markdown(res["description"], unsafe_allow_html=True)

    if st.button("Confirmar Devolución", use_container_width=True):
        conn = st.connection('biblionline_db', type='sql')
        with conn.session as s:
            # Consulta SQL para eliminar el libro prestado
            query = text("""
                DELETE FROM rented_books 
                WHERE user_id = :user_id AND book_title = :book_title
            """)
            s.execute(query, {
                'user_id': st.session_state.user["id"],
                'book_title': res["title"]
            })
            s.commit()
        st.success(f"Libro '{res['title']}' devuelto correctamente.")
        st.experimental_rerun()  # Actualiza la interfaz

# Mostrar la página de libros prestados
show_rented_books()