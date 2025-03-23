import streamlit as st

pg = st.navigation(["pages/page_view_books.py","pages/page_login.py", "pages/page_register.py"])
pg.run()