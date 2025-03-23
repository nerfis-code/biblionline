import streamlit as st

from apis import books
st.title("Estoy viendo los libros")

st.code(books.search(),wrap_lines=True)