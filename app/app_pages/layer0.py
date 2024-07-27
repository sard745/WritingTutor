import streamlit as st
from session_state import layer_session, title_session, source_session
from functools import partial

def layer_0(db, i):
  data = db.get_level(i)

  for idx in range(data.shape[0]):
    title = data.title.values[idx]
    path = data.path.values[idx]
    with st.expander(data.title.values[idx]):
      st.write(data.beginning.values[idx])
      st.button(label="Try", key=f"button_{title}", on_click=partial(lambda x,y,z :[layer_session(x), title_session(y), source_session(z)], 1, title, path))