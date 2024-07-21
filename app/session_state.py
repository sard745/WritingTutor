import streamlit as st

def layer_session(layer=0):
    st.session_state.layer=layer

def summary_session(summary=None):
   st.session_state.summary=summary

def reg_session(reg=False):
    st.session_state.reg=reg

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
        # print("セッション変更なし")
        # print(f"セッション変更前 {st.session_state.not_change}")
        not_change_session()
        # print(f"セッション変更後 {st.session_state.not_change}")
        return
    st.session_state.now_layer=None
    st.session_state.now_menu=None
    not_change_session()
    layer_session()
    source_session()
    title_session()
    summary_session()
    reg_session()
    # print(f"セッション変更2 {st.session_state.not_change}")