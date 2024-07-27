import streamlit as st
from session_state import not_change_session, add_session
from components.back_btn import back_btn


def add_source_text(db):
   with st.form("form"):
      title = st.text_input("Title")
      text = st.text_area("Source Text", height=400)
      level = st.selectbox("Select Level", [1,2,3,4,5], format_func=lambda i: f"Level {i}")

      reg = st.form_submit_button("register", on_click=lambda:[not_change_session(True)])
   
   if reg:
      print(f"title: {title}, text: {text}, level: {level}")
      if title == "" or text == "" or level == None:
         print("error")
         st.error("Please fill in all fields")
         add_session(True)
      else:
         db.add_text(title, level, text)
         add_session(False)
         st.success("Successfully registered")
   back_btn(lambda:add_session(False))