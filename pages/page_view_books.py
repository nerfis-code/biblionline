import streamlit as st
from apis import books


@st.dialog("Libro",width="large")
def view_book(res):
    col1, col2 = st.columns(2)
    with col1:
        st.title(res["title"])
        st.image(res["cover"])
        if st.button("Rentar"):
            # st.session_state.vote = {"item": item, "reason": reason}
            st.rerun()
    with col2:
        st.title("Sumary")
        st.markdown(res["description"],unsafe_allow_html=True)
        
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
        if container.button("Rentar", key=res["id"]): 
            view_book(res)
    colIndex += 1
    colIndex %= len(cols)

