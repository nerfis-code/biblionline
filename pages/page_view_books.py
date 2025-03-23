import streamlit as st

from apis import books
st.title("Estoy viendo los libros")

col1, col2, col3, col4 = st.columns(4)
cols = [col1,col2,col3,col4,]

response = books.search()["books"]
st.code(response,wrap_lines=True)

colIndex = 0
for res in response:
    with cols[colIndex]:
        container = st.container(border=True)
        container.image(res["cover"])
    colIndex += 1
    colIndex %= len(cols)

