import streamlit as st

def layer_session(layer=0):
    # print(f"change layer, from {st.session_state.layer} to {layer}" 
    st.session_state.layer=layer

def summary_session(summary=None):
   st.session_state.summary=summary

def add_session(add=False):
    st.session_state.add_cont=add

def not_change_session(not_change=False):
    # print("---------------")
    # print("not change")
    st.session_state.not_change=not_change

def observe_session():
    if st.session_state.now_menu!=st.session_state.menu:
    #   print("observe_menu")
      reset_session()
    elif st.session_state.now_layer==st.session_state.layer:
    #   print("observe_layer")
      reset_session()

    st.session_state.now_menu=st.session_state.menu
    st.session_state.now_layer=st.session_state.layer

def source_session(source=None):
    st.session_state.source=source

def title_session(title=None):
    st.session_state.title=title
  
def reset_session():
    if ("not_change" in st.session_state.keys()) and st.session_state.not_change:
        not_change_session()
        return
    st.session_state.now_layer=None
    st.session_state.now_menu=None
    not_change_session()
    layer_session()
    source_session()
    title_session()
    summary_session()
    add_session()