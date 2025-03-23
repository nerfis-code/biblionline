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

def exist_user(username,password):
    with conn.session as s:
        # Query the database
        result = s.execute("SELECT * FROM users WHERE username=:username and password=:password;",
                           params={"username":username,"password":password})
        
        # Display the result
        return len(result.fetchall()) == 1
    
def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        
    if not st.session_state.logged_in:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar"):
            
            if exist_user(username,password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
        return False
    return True

if check_login():
    st.markdown("## ¡Bienvenido Admin !")
    # Tu contenido aquí...
    ...