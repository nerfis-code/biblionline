import streamlit as st

from apis import books
st.title("Estoy viendo los libros")
text_search = st.text_input("Search videos by title or speaker", value="")
if text_search:
    response = books.search(text_search)["books"]
else:
    response = books.search("batman")["books"]  
    
col1, col2, col3, col4 = st.columns(4)
cols = [col1,col2,col3,col4,]

st.code(response,wrap_lines=True)

colIndex = 0
for res in response:
    with cols[colIndex]:
        container = st.container(border=True)
        container.image(res["cover"])
    colIndex += 1
    colIndex %= len(cols)

