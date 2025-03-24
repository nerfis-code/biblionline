import streamlit as st
from sqlalchemy import text
import hashlib  # Añadido para cifrar la contraseña
import components

components.nav()
def show_user_profile():
    
    if 'user' not in st.session_state:
        st.error("Debes iniciar sesión para ver esta página")
        st.page_link("pages/1_login.py", label="Ir a inicio de sesión")
        return

    # Conexión a la base de datos
    conn = st.connection('biblionline_db', type='sql')
    
    # Obtener datos actuales del usuario
    with conn.session as session:
        user_data = session.execute(
            text("SELECT * FROM users WHERE id = :user_id"),
            {"user_id": st.session_state.user["id"]}
        ).mappings().first()

    if not user_data:
        st.error("Usuario no encontrado")
        return

    # Mostrar información del usuario
    st.title("👤 Mi Perfil")
    
    with st.form("user_profile_form"):
        cols = st.columns(2)
        
        # Campos editables
        new_name = cols[0].text_input("Nombre", value=user_data['name'])
        new_email = cols[1].text_input("Email", value=user_data['email'])
        new_password = st.text_input("Nueva contraseña", type="password")
        confirm_password = st.text_input("Confirmar contraseña", type="password")
        
        # Sección para subir avatar
        uploaded_file = st.file_uploader("Cambiar avatar", type=["jpg", "png"])
        
        if st.form_submit_button("Guardar cambios"):
            # Validaciones
            if new_password and new_password != confirm_password:
                st.error("Las contraseñas no coinciden")
                return
                
            try:
                # Actualizar datos en la base de datos
                with conn.session as session:
                    update_query = text("""
                        UPDATE users 
                        SET name = :name, email = :email
                        WHERE id = :user_id
                    """)
                    params = {
                        "name": new_name,
                        "email": new_email,
                        "user_id": st.session_state.user["id"]
                    }
                    
                    # Si se proporcionó nueva contraseña
                    if new_password:
                        # Cifrar la contraseña utilizando hashlib.sha256 (igual que en login)
                        hashed_password = hashlib.sha256(new_password.strip().encode()).hexdigest()
                        update_query = text("""
                            UPDATE users 
                            SET name = :name, email = :email, password = :password
                            WHERE id = :user_id
                        """)
                        params["password"] = hashed_password
                    
                    session.execute(update_query, params)
                    session.commit()
                    
                    # Actualizar datos en sesión
                    st.session_state.user.update({
                        "name": new_name,
                        "email": new_email
                    })
                    
                    # Si se cambió contraseña, actualizar en sesión también
                    if new_password:
                        st.session_state.user["password"] = hashlib.sha256(new_password.strip().encode()).hexdigest()
                    
                    # Manejar la imagen subida
                    if uploaded_file:
                        # Aquí iría la lógica para guardar el archivo
                        # Por ejemplo: guardar en storage o en la base de datos
                        st.session_state.user["avatar"] = uploaded_file.read()
                    
                    st.success("Perfil actualizado correctamente!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error al actualizar perfil: {str(e)}")


# Mostrar la página
show_user_profile()