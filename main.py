import streamlit as st

pg = st.navigation(["pages/page_view_books.py","pages/page_book_collection.py","pages/page_login.py", "pages/page_register.py", "pages/user_page.py"])
pg.run()