import streamlit as st

st.text(st.session_state)
if not "logged_in" in st.session_state or not st.session_state.logged_in:
    st.title("Necesitas iniciar sesion para poder ver tu colecion de libros")
else:
    st.title("Colecion de libros")