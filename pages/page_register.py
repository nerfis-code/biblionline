import streamlit as st
from sqlalchemy import text
import hashlib

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
            
            try:
                # Verificar si el usuario ya existe
                session = conn.session

                result = session.execute(text("""
                    SELECT 1 FROM users WHERE username = :user OR email = :email
                """), {'user': username, 'email': email})

                user_exists = result.fetchone()  # Obtiene el primer resultado si existe

                if user_exists:
                    st.error("El usuario o email ya están registrados")
                    return
                
                # Insertar nuevo usuario
                hashed_pw = hashlib.sha256(password.strip().encode()).hexdigest()
                
                session.execute(text("""
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
                session.commit()
                
                st.success("¡Registro exitoso! Redirigiendo...")
                st.session_state.show_register = True
                st.rerun()
                
            except Exception as e:
                st.error(f"Error al registrar: {str(e)}")

            finally:
                session.close()

        # Enlace para volver al login
        
        st.markdown('<a href="page_login" target="_self">¿Ya tienes cuenta? Inicia sesión aquí</a>',
                    unsafe_allow_html=True)

if show_register():
    st.markdown("## ¡Bienvenido!")
