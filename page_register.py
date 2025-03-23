# auth_registro.py
import streamlit as st
from sqlalchemy import text
import hashlib

def mostrar_registro():
    conn = st.connection('biblionline_db', type='sql')
    
    with st.form("Formulario de Registro"):
        st.subheader("Crear Nueva Cuenta")
        
        nombre = st.text_input("Nombre*")
        apellido = st.text_input("Apellido*")
        username = st.text_input("Nombre de usuario*")
        email = st.text_input("Email*")
        password = st.text_input("Contraseña*", type="password")
        repetir_password = st.text_input("Repetir contraseña*", type="password")
        
        submitted = st.form_submit_button("Registrarse")
        
        if submitted:
            # Validaciones
            if not all([nombre, apellido, username, email, password]):
                st.error("Todos los campos marcados con * son obligatorios")
                return
                
            if password != repetir_password:
                st.error("Las contraseñas no coinciden")
                return
            
            try:
                # Verificar si el usuario ya existe
                user_exists = conn.query(
                    "SELECT 1 FROM users WHERE username = :user OR email = :email",
                    params={'user': username, 'email': email},
                    ttl=0
                )
                
                if not user_exists.empty:
                    st.error("El usuario o email ya están registrados")
                    return
                
                # Insertar nuevo usuario
                hashed_pw = hashlib.sha256(password.encode()).hexdigest()
                
                with conn.session as session:
                    session.execute(text("""
                        INSERT INTO users 
                        (nombre, apellido, username, email, password)
                        VALUES (:nombre, :apellido, :username, :email, :password)
                    """), {
                        'nombre': nombre,
                        'apellido': apellido,
                        'username': username,
                        'email': email,
                        'password': hashed_pw
                    })
                    session.commit()
                
                st.success("¡Registro exitoso! Redirigiendo...")
                st.session_state.mostrar_login = True
                st.rerun()
                
            except Exception as e:
                st.error(f"Error al registrar: {str(e)}")

        # Enlace para volver al login
        st.markdown("[¿Ya tienes cuenta? Inicia sesión aquí](#login)")


