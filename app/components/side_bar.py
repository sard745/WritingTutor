import streamlit as st
from session_state import not_change_session

def side_bar():
  with st.sidebar:
    st.sidebar.write("Settings")
    st.sidebar.write("---")
    st.session_state.model = st.sidebar.radio("select gpt model", ["gpt-3.5", "gpt-4"], on_change=lambda:[not_change_session(True)])
    st.sidebar.write("---")
    st.sidebar.write("select evaluate")

    st.sidebar.toggle("coherence", key="coherence", value=True, on_change=lambda:[not_change_session(True)])
    st.sidebar.toggle("consistency", key="consistency", value=True, on_change=lambda:[not_change_session(True)])
    st.sidebar.toggle("fluency", key="fluency", value=True, on_change=lambda:[not_change_session(True)])
    st.sidebar.toggle("relevance", key="relevance", value=True, on_change=lambda:[not_change_session(True)])

    st.sidebar.write("---")
    st.sidebar.button("register source", key="add")