import hashlib
import streamlit as st
import components



conn = st.connection('biblionline_db', type='sql')


components.nav()
def exist_user(username,password):
    with conn.session as s:
        result = s.execute("SELECT * FROM users WHERE username=:username and password=:password;",
                           params={"username":username,"password":hashlib.sha256(password.strip().encode()).hexdigest()})
        
        return result.fetchone()
    
def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        
    if not st.session_state.logged_in:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        st.page_link("pages/2_register.py", label="¿Todavia no tienes cuenta? que esperas!")
        if st.button("Ingresar"):
            user = exist_user(username,password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = {"id": user[0],
                                         "username": user[1],
                                         "password": user[2],
                                         "name": user[3],
                                         "lastname": user[4],
                                         "email": user[5],
                                         }
                
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
        return False
    return True

if check_login():
    name = st.session_state.user["name"] if st.session_state.user["name"] else st.session_state.user["username"]
    st.markdown(f"## ¡Bienvenido {name} !")
    
    ...
