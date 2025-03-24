import streamlit as st
import sqlite3
from datetime import datetime
import os
from PIL import Image

def get_user_data(user_id):
    conn = st.connection('biblionline_db', type='sql')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_user_profile(user_id, full_name, bio, profile_pic):
    conn = st.connection('biblionline_db', type='sql')
    c = conn.cursor()
    c.execute('''UPDATE users 
                 SET full_name = ?, bio = ?, profile_pic = ?
                 WHERE user_id = ?''',
              (full_name, bio, profile_pic, user_id))
    conn.commit()
    conn.close()

def save_profile_pic(uploaded_file, user_id):
    if uploaded_file is not None:
        # Generar nombre único
        ext = uploaded_file.name.split('.')[-1]
        filename = f"{user_id}_profile.{ext}"
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Guardar imagen
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Redimensionar imagen
        img = Image.open(save_path)
        img.thumbnail((200, 200))
        img.save(save_path)
        
        return filename
    return None

def show_user_dashboard():
    st.title("👤 Perfil de Usuario")
    
    if 'user_id' not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta página")
        return
    
    user_data = get_user_data(st.session_state.user_id)
    
    # Mostrar información del usuario
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if user_data[5]:  # profile_pic
            st.image(os.path.join(UPLOAD_FOLDER, user_data[5]), 
                    width=200)
        else:
            st.image("default_profile.png", width=200)
            
        st.write(f"Miembro desde: {user_data[7][:10]}")
    
    with col2:
        st.subheader(user_data[3] or "Sin nombre")
        st.write(user_data[4] or "Sin biografía")
    
    # Sección de edición de perfil
    with st.expander("✏️ Editar Perfil"):
        with st.form("profile_form"):
            full_name = st.text_input("Nombre completo", 
                                     value=user_data[3] or "")
            bio = st.text_area("Biografía", 
                              value=user_data[4] or "")
            new_pic = st.file_uploader("Nueva foto de perfil", 
                                      type=['jpg', 'png', 'jpeg'])
            
            if st.form_submit_button("💾 Guardar Cambios"):
                profile_pic = save_profile_pic(new_pic, 
                                              st.session_state.user_id)
                # Mantener la imagen actual si no se sube nueva
                if not profile_pic and user_data[5]:
                    profile_pic = user_data[5]
                
                update_user_profile(st.session_state.user_id,
                                   full_name, 
                                   bio, 
                                   profile_pic)
                st.success("Perfil actualizado correctamente!")
                st.rerun()
    
    # Sección de libros alquilados
    st.header("📚 Libros Alquilados")
    conn = sqlite3.connect(DATABASE)
    rentals = conn.execute('''SELECT book_title, rental_date 
                            FROM rentals 
                            WHERE user_id = ? 
                            ORDER BY rental_date DESC''',
                         (st.session_state.user_id,)).fetchall()
    conn.close()
    
    if rentals:
        for book, date in rentals:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                col1.subheader(book)
                col2.write(f"Alquilado el: {date[:10]}")
    else:
        st.warning("No tienes libros alquilados actualmente")

# Inicializar la base de datos al inicio
DATABASE = "biblionline.db"

# Ejecutar la aplicación
if __name__ == "__main__":
    # Simular usuario logueado (eliminar en producción)
    st.session_state.user_id = 1  
    
    show_user_dashboard()