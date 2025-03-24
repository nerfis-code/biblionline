import streamlit as st

default = {
    "user":None,
    "logged_in":False
}


def nav():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.page_link("View_books.py", label="vista de libros", icon="🏠")
    with col2:
        st.page_link(
                "pages/3_user.py" if "user" in st.session_state and st.session_state.user else 
                "pages/1_login.py",
            label="Usuario", icon="👤")
    with col3:
        st.page_link("pages/4_book_collection.py", label="coleccion", icon="📖")
        
def set_local_storage(key, value):
    st.html(f"""
    <script>
    localStorage.setItem('{key}', '{value}');
    </script>
    """, height=0)

# Leer de localStorage
def get_local_storage(key):
    html_str = f"""
    <script>
    var value = localStorage.getItem('{key}');
    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: value}}, '*');
    </script>
    """
    return st.html(html_str, height=0)