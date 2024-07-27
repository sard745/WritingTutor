from session_state import layer_session
import streamlit as st

# UI components
def deco_horizontal(func):
    def wrapper(*args, **kwargs):
        st.write("---")
        func(*args, **kwargs)
        st.write("---")
    return wrapper

@deco_horizontal
def back_btn(func=lambda:layer_session(st.session_state.layer-1)):
    st.button(f"back", on_click=func)