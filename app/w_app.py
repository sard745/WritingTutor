from session_state import layer_session, summary_session, observe_session, source_session, title_session, reset_session
from option_menu import get_option_menu
from hide_st import hide_st
from side_button import create_checkbox_group
import streamlit as st
import sqlite3
import pandas as pd
import time
from functools import partial

LEVELS = [f"Level {i}" for i in range(1,6)]

SET_PAGE_CONFIG = {
    "page_title": "Streamlit Base",
    "page_icon": "😀",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}

def init():
  if "init" not in st.session_state:
    st.session_state.init=True
    reset_session()
    return True
  else:
    return False

def load_level(db_name, i):
  select_all_sql = 'select ' + '*' + ' from ' + 'source_text' + ' where level = ' + str(i)
  
  with sqlite3.connect(db_name) as conn:
    df_from_sql = pd.read_sql(select_all_sql, conn)

  return df_from_sql

def layer_0(i):
  data = df_from_sql
  res = [False] * df_from_sql[:5-i].shape[0]

  for idx in range(df_from_sql[:5-i].shape[0]):
    title = data.title.values[idx]
    path = data.path.values[idx]
    with st.expander(data.title.values[idx]):
      # TODO: データベースから取得するように変更
      with open(data.path.values[idx], "r") as f:
        lines = f.read()
      st.write(lines[:200])
      st.button(label="Try", key=f"button_{title}", on_click=partial(lambda x,y,z :[layer_session(x), title_session(y), source_session(z)], 1, title, path))

def layer_1(title, path):
  st.write(title)
  with open(path, "r") as f:
    s_text = f.read()
  col1, col2 = st.columns(2)

  source = col1.text_area(
            ":black[Source text]",
            value=f'{s_text}',
            height=400,
        )

  summary = col2.text_area(
            "Summary", 
            value="Summarize source text here.",
            height=400
        )
  
  st.button("apply", on_click=lambda:[summary_session(summary),layer_session(2)])

def layer_2(title, source, input):
  st.write(title)
  col1, col2 = st.columns(2)
  with open(source, "r") as f:
      s_text = f.read()

  source = col1.text_area(
            ":black[Source text]",
            value=f'{s_text}',
            height=400,
        )

  summary = col2.text_area(
            "Summary", 
            value=input,
            height=400
        )
  
  st.write("---")
  st.markdown("- Coherence: 1  \nGreat!\n- Grammar: 1  \nBad!")
  st.write("---")


db_name = "/home/work/db/source_text.db"

select_all_sql = 'select ' + '*' + ' from ' + 'source_text'
with sqlite3.connect(db_name) as conn:
    df_from_sql = pd.read_sql(select_all_sql, conn)

#列名を取り出す
df_from_sql_columns = df_from_sql.columns

st.set_page_config(**SET_PAGE_CONFIG)

st.markdown(
        "<h1 style='text-align: center;'>Writing Tutor</h1>",
        unsafe_allow_html=True,
    )

init()

# st.session_state.ck=0

st.sidebar.write("Settings")
st.session_state.model = st.sidebar.radio("select gpt model", ["gpt-3.5", "gpt-4"])

def menu(key):
  reset_session()

st.session_state.menu = get_option_menu(LEVELS)

all_button = "all"
part_button_list = ["coherence", "consistency", "fluency", "relevance"]
create_checkbox_group(all_button, part_button_list, "select evaluate", st.sidebar)

observe_session()

_layer = st.session_state.layer
_source = st.session_state.source
_level = st.session_state.menu
_title = st.session_state.title
_sum = st.session_state.summary
_coh = st.session_state["coherence"]
_con = st.session_state["consistency"]
_flu = st.session_state["fluency"]
_rel = st.session_state["relevance"]


time.sleep(0.1)

if _level == "Level 1":
  print(f"Level 1: {_layer} {_title}, {_source}")
  print(f"coherence: {_coh}, consistency: {_con}, fluency: {_flu}, relevance: {_rel}")
  st.empty()
  if _layer==0:
    layer_0(1)
  elif _layer==1:
    layer_1(_title, _source)
  elif _layer==2:
    layer_2(_title, _source, _sum)

elif _level == "Level 2":
  st.empty()
  print(f"Level 2: {_layer} {_title}, {_source}")
  if _layer==0:
    layer_0(2)
  elif _layer==1:
    layer_1(_title, _source)