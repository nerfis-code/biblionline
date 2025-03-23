import hashlib
import streamlit as st


conn = st.connection('biblionline_db', type='sql')

with conn.session as s:
    result = s.execute("SELECT * FROM users")
    st.write(result.fetchall())


def exist_user(username,password):
    with conn.session as s:
        result = s.execute("SELECT 1 FROM users WHERE username=:username and password=:password;",
                           params={"username":username,"password":hashlib.sha256(password.strip().encode()).hexdigest()})
        
        return result.fetchone()
    
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
    ...