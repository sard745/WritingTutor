import streamlit as st

def layer_session(layer=0):
    st.session_state.layer=layer

def summary_session(summary=None):
   st.session_state.summary=summary

def observe_session():
    if not st.session_state.now_menu==st.session_state.menu:
      reset_session()
    elif st.session_state.now_layer==st.session_state.layer:
      reset_session()

    st.session_state.now_menu=st.session_state.menu
    st.session_state.now_layer=st.session_state.layer

def source_session(source=None):
    st.session_state.source=source

def title_session(title=None):
    st.session_state.title=title
  
def reset_session():
    print("call reset_session")
    st.session_state.now_layer=None
    st.session_state.now_menu=None
    layer_session()
    source_session()
    title_session()
    summary_session()