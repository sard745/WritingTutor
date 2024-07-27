from app_pages import layer0, layer1, layer2, add_source
from db.database import SourceTextDB
import streamlit as st
from session_state import reset_session, not_change_session, observe_session, add_session
from components.option_menu import get_option_menu
import time
import re
from components.side_bar import side_bar
from hide_st import hide_st

LEVELS = [f"Level {i}" for i in range(1,6)]
SCORING_ITEMS = ["coherence", "consistency", "fluency", "relevance"]
SET_PAGE_CONFIG = {
    "page_title": "Writing Tutor",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}

db_name = "/home/work/db/source_text.db"
db = SourceTextDB(db_name)

def init():
  if "init" not in st.session_state:
    st.session_state.init=True
    reset_session()
    return True
  else:
    return False
  
if __name__ == "__main__":
  st.set_page_config(**SET_PAGE_CONFIG)
  hide_st()
  st.markdown(
        "<h1 style='text-align: center;'>Writing Tutor</h1>",
        unsafe_allow_html=True,
    )
  
  init()

  st.session_state.menu = get_option_menu(LEVELS)

  side_bar()

  observe_session()

  _layer = st.session_state.layer
  _source = st.session_state.source
  _level = st.session_state.menu
  _title = st.session_state.title
  _sum = st.session_state.summary
  _add_cont = st.session_state.add_cont
  _add = st.session_state.add

  time.sleep(0.1)

  if _add or _add_cont:
    add_session(True)
    add_source.add_source_text(db)
  
  else:
    st.empty()
    level = re.findall(r"Level (\d)", _level)[0]
    if _layer == 0:
      layer0.layer_0(db, level)
    elif _layer == 1:
      layer1.layer_1(_title, _source, SCORING_ITEMS)
    elif _layer == 2:
      layer2.layer_2(_title, _source, _sum, SCORING_ITEMS)
    else:
      st.write("Error")
