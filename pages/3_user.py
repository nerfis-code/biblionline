import streamlit as st
from sqlalchemy import text
import hashlib  # Añadido para cifrar la contraseña
import components

st.set_page_config(
    page_icon="⚓"
)
components.nav()
def show_user_profile():
    
    if 'user' not in st.session_state:
        st.error("Debes iniciar sesión para ver esta página")
        st.page_link("pages/1_login.py", label="Ir a inicio de sesión")
        return

    conn = st.connection('biblionline_db', type='sql')
    
    with conn.session as session:
        user_data = session.execute(
            text("SELECT * FROM users WHERE id = :user_id"),
            {"user_id": st.session_state.user["id"]}
        ).mappings().first()

    if not user_data:
        st.error("Usuario no encontrado")
        return

    st.title("👤 Mi Perfil")
    
    with st.form("user_profile_form"):
        cols = st.columns(2)
        
        new_name = cols[0].text_input("Nombre", value=user_data['name'])
        new_email = cols[1].text_input("Email", value=user_data['email'])
        new_password = st.text_input("Nueva contraseña", type="password")
        confirm_password = st.text_input("Confirmar contraseña", type="password")
        
        
        
        if st.form_submit_button("Guardar cambios"):
            if new_password and new_password != confirm_password:
                st.error("Las contraseñas no coinciden")
                return
                
            try:
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
                    
                    if new_password:
                        hashed_password = hashlib.sha256(new_password.strip().encode()).hexdigest()
                        update_query = text("""
                            UPDATE users 
                            SET name = :name, email = :email, password = :password
                            WHERE id = :user_id
                        """)
                        params["password"] = hashed_password
                    
                    session.execute(update_query, params)
                    session.commit()
                    
                    st.session_state.user.update({
                        "name": new_name,
                        "email": new_email
                    })
                    
                    if new_password:
                        st.session_state.user["password"] = hashlib.sha256(new_password.strip().encode()).hexdigest()
                    
                    
                    
                    st.success("Perfil actualizado correctamente!")
                    
            except Exception as e:
                st.error(f"Error al actualizar perfil: {str(e)}")
    if st.button("Salir de la cuenta"):
        del st.session_state.user
        st.rerun()

# Mostrar la página
show_user_profile()