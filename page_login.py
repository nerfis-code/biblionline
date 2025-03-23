import streamlit as st
from sqlalchemy import create_engine, text
# Create the SQL connection to biblionline_db as specified in your secrets file.
conn = st.connection('biblionline_db', type='sql')

with conn.session as s:
    # Query the database
    result = s.execute("SELECT * FROM users")
    # Display the result
    st.write(result.fetchall())

@st.dialog("Felitaciones tienes una cuenta")
def login():
    st.write(f"Bienvenido {"Admin"}")


def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        
    if not st.session_state.logged_in:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar"):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                login()
            else:
                st.error("Credenciales incorrectas")
        return False
    return True

if check_login():
    st.markdown("## ¡Bienvenido a tu aplicación!")
    # Tu contenido aquí...
    ...