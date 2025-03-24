import streamlit as st
from sqlalchemy import text
import hashlib
import components

components.nav()
def show_register():
    conn = st.connection('biblionline_db', type='sql')
    
    with st.form("Formulario de Registro"):
        st.subheader("Crear Nueva Cuenta")
        
        name = st.text_input("Nombre*")
        lastname = st.text_input("Apellido*")
        username = st.text_input("Nombre de usuario*")
        email = st.text_input("Email*")
        password = st.text_input("Contraseña*", type="password")
        copy_password = st.text_input("Repetir contraseña*", type="password")
        
        submitted = st.form_submit_button("Registrarse")
        
        if submitted:
            # name, lastname y email ya no seran necesarias
            if not all([username, password]):
                st.error("usuario y la contraseña son obligatorios")
                return
                
            if password != copy_password:
                st.error("Las contraseñas no coinciden")
                return
            with conn.session as s:
                # Verificar si el usuario ya existe

                result = s.execute(text("""
                    SELECT 1 FROM users WHERE username = :user
                """), {'user': username})

                user_exists = result.fetchone()  # Obtiene el primer resultado si existe

                if user_exists:
                    st.error("El usuario ya están registrados")
                    return
                
                # Insertar nuevo usuario
                hashed_pw = hashlib.sha256(password.strip().encode()).hexdigest()
                
                s.execute(text("""
                    INSERT INTO users 
                    (name, lastname, username, email, password)
                    VALUES (:name, :lastname, :username, :email, :password)
                """), {
                    'name': name.strip() if name.strip() != "" else None,
                    'lastname': lastname.strip() if lastname.strip() != "" else None,
                    'username': username.strip(),
                    'email': email.strip() if email.strip() != "" else None,
                    'password': hashed_pw
                    })
                s.commit()
                
            st.success("¡Registro exitoso! Redirigiendo...")
            st.session_state.show_register = True
            st.balloons()
            st.rerun()

        st.page_link("pages/1_login.py", label="¿Ya tienes cuenta? Inicia sesión aquí")


if show_register():
    st.markdown("## ¡Bienvenido!")
    st.link_button(url="pages/1_login.py",label="Empieza tu aventura iniciando sesion")
