import streamlit as st

# Create the SQL connection to biblionline_db as specified in your secrets file.
conn = st.connection('biblionline_db', type='sql')

with conn.session as s:
    # Query the database
    result = s.execute("SELECT * FROM Users")
    # Display the result
    st.write(result.fetchall())

   