from session_state import layer_session, summary_session, observe_session, source_session, title_session, reset_session, not_change_session, reg_session
from option_menu import get_option_menu
from hide_st import hide_st
from side_button import create_checkbox_group
import streamlit as st
import sqlite3
import pandas as pd
import time
from functools import partial
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import os
import sys
sys.path.append(os.getcwd())
from db.database import SourceTextDB
from evaluator import evaluator
import yaml
import json

LEVELS = [f"Level {i}" for i in range(1,6)]

db_name = "/home/work/db/source_text_copy.db"
db = SourceTextDB(db_name)

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

def format_func(i):
  return f"Level {i}"

def add_source_text():
   title = st.text_input("Title", on_change=lambda:[not_change_session(True)])
   text = st.text_area("Source Text", height=400, on_change=lambda:[not_change_session(True)])
   level = st.selectbox("Select Level", [1,2,3,4,5], format_func=format_func, on_change=lambda:[not_change_session(True)])

   st.button("register", on_click=lambda:[db.add_text(title, level, text)])

def layer_0(i):
  data = db.get_level(i)

  for idx in range(data.shape[0]):
    title = data.title.values[idx]
    path = data.path.values[idx]
    with st.expander(data.title.values[idx]):
      st.write(data.beginning.values[idx])
      st.button(label="Try", key=f"button_{title}", on_click=partial(lambda x,y,z :[layer_session(x), title_session(y), source_session(z)], 1, title, path))

def layer_1(title, path):
  st.write(title)
  with open(path, "r") as f:
    s_text = f.read()
  # col1, col2 = st.columns(2)

  # source = col1.text_area(
  #           ":black[Source text]",
  #           value=f'{s_text}',
  #           height=400,
  #           on_change=lambda:[not_change_session(True)]
  #       )
  
  # summary_key = "summary_text"
  # if summary_key not in st.session_state:
  #   st.session_state[summary_key] = "Summarize source text here."
  col1, col2 = st.columns(2)
  with st.form("form"):
  # col1, col2 = form.columns(2)
    col1, col2 = st.columns(2)

    with col1:
      st.text_area(
                  ":black[Source text]",
                  value=f'{s_text}',
                  height=400,
                  # on_change=lambda:[not_change_session(True)]
              )
      
    with col2:
      st.text_area(
                  "Summary", 
                  key = "summary",
                  # value=st.session_state[summary_key],
                  height=400,
                  # on_change=lambda:[not_change_session(True)]
              )
      
    # st.form_submit_button("apply", on_click=lambda:[evaluate(s_text, st.session_state.summary), layer_session(2)])
    st.form_submit_button("apply", on_click=lambda:[layer_session(2)])
  
  back_btn()

  # if submit:
  #   print("submit")
  #   print(st.session_state.summary)
  #   not_change_session(True)
  # st.write(st.session_state.summary)

  # st.button("apply", on_click=lambda:[summary_session(summary), evaluate(source, summary), layer_session(2)])
  # st.form_submit_button("apply", on_click=lambda:[summary_session(summary), print(st.session_state.summary)])

def layer_2(title, source, input):
  st.write(title)
  col1, col2 = st.columns(2)
  with open(source, "r") as f:
      s_text = f.read()

  col1.text_area(
            ":black[Source text]",
            value=f'{s_text}',
            height=400,
            on_change=lambda:[not_change_session(True)]
        )

  col2.text_area(
            "Summary", 
            value=input,
            height=400,
            on_change=lambda:[not_change_session(True)]
        )
  
  st.write("---")
  st.write("Feedback")
  # if st.session_state.feedback_coh is not None:
  #   st.markdown(f"- Coherence: {st.session_state.feedback_coh['rating']}  \n{st.session_state.feedback_coh['analysis']}")
  # if st.session_state.feedback_con is not None:
  #   st.markdown(f"- Consistency: {st.session_state.feedback_con['rating']}  \n{st.session_state.feedback_con['analysis']}")
  # if st.session_state.feedback_flu is not None:
  #   st.markdown(f"- Fluency: {st.session_state.feedback_flu['rating']}  \n{st.session_state.feedback_flu['analysis']}")
  # if st.session_state.feedback_rel is not None:
  #   st.markdown(f"- Relevance: {st.session_state.feedback_rel['rating']}  \n{st.session_state.feedback_rel['analysis']}")
  st.write("---")
  back_btn()

# UI components
def deco_horizontal(func):
    def wrapper(*args, **kwargs):
        st.write("---")
        func(*args, **kwargs)
        st.write("---")
    return wrapper

@deco_horizontal
def back_btn():
    st.button(f"back",on_click=layer_session(_layer-1))

def evaluate(source, summary):
  if st.session_state.model == "gpt-3.5":
    with open("/home/work/evaluator/configs/gpt3_5.yaml", "r") as f:
      config = yaml.safe_load(f)
  else:
    with open("/home/work/evaluator/configs/gpt3_5.yaml", "r") as f:
      config = yaml.safe_load(f)

  with open("/home/work/evaluator/prompt/system_prompt.txt", "r") as f:
    system_prompt = f.read()

  with open("/home/work/evaluator/prompt/user_prompt.txt", "r") as f:
    user_prompt = f.read()


  print(f"run: Coherence={coherence}, Consistency={consistency}, Fluency={fluency}, Relevance={relevance}")

  # for criteria in [coherence, consistency, fluency, relevance]:
  #   if criteria:
  #     with open("/home/work/evaluator/prompt/criteria/coherence.json", "r") as f:
  #       criteria = json.load(f)
  #     feedback = evaluator.run(config, source, system_prompt, criteria, summary)
  #     # result[criteria] = (feedback["analysis"], feedback["rating"])
  #     st.session_state[criteria] = feedback
  #   else:
  #     st.session_state
  if coherence:
    with open("/home/work/evaluator/prompt/criteria/coherence.json", "r") as f:
        criteria = json.load(f)
    feedback = evaluator.run(config, source, system_prompt, user_prompt, criteria, summary)
      # result[criteria] = (feedback["analysis"], feedback["rating"])
    print(feedback)
    st.session_state.feedback_coh = feedback
  else:
    st.session_state.feedback_coh = None

  if consistency:
    with open("/home/work/evaluator/prompt/criteria/consistency.json", "r") as f:
        criteria = json.load(f)
    feedback = evaluator.run(config, source, system_prompt, user_prompt, criteria, summary)
      # result[criteria] = (feedback["analysis"], feedback["rating"])
    st.session_state.feedback_con = feedback
  else:
    st.session_state.feedback_con = None

  if fluency:
    with open("/home/work/evaluator/prompt/criteria/fluency.json", "r") as f:
        criteria = json.load(f)
    feedback = evaluator.run(config, source, system_prompt, user_prompt, criteria, summary)
      # result[criteria] = (feedback["analysis"], feedback["rating"])
    st.session_state.feedback_flu = feedback
  else:
    st.session_state.feedback_flu = None

  if relevance:
    with open("/home/work/evaluator/prompt/criteria/relevance.json", "r") as f:
        criteria = json.load(f)
    feedback = evaluator.run(config, source, system_prompt, user_prompt, criteria, summary)
      # result[criteria] = (feedback["analysis"], feedback["rating"])
    st.session_state.feedback_rel = feedback
  else:
    st.session_state.feedback_rel = None


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

names = ['John Smith', 'Rebecca Briggs']  # 
usernames = ['jsmith', 'rbriggs']  # 入力フォームに入力された値と合致するか確認される
passwords = ['123', '456']  # 入力フォームに入力された値と合致するか確認される

# パスワードをハッシュ化。 リスト等、イテラブルなオブジェクトである必要がある
hashed_passwords = Hasher(passwords).generate()

credentials = {"usernames":{}}

for un, name, pw in zip(usernames, names, hashed_passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})

init()

# cookie_expiry_daysでクッキーの有効期限を設定可能。認証情報の保持期間を設定でき値を0とするとアクセス毎に認証を要求する
authenticator = stauth.Authenticate(credentials,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

# print(f"ログイン状態 {st.session_state['authentication_status']}")

st.sidebar.write("Settings")
st.sidebar.write("---")
st.session_state.model = st.sidebar.radio("select gpt model", ["gpt-3.5", "gpt-4"], on_change=lambda:[not_change_session(True)])

st.session_state.menu = get_option_menu(LEVELS)

all_button = "all"
part_button_list = ["coherence", "consistency", "fluency", "relevance"]
st.sidebar.write("---")
st.sidebar.write("select evaluate")
coherence = st.sidebar.toggle("coherence", on_change=lambda:[not_change_session(True)])
consistency = st.sidebar.toggle("consistency", on_change=lambda:[not_change_session(True)])
fluency = st.sidebar.toggle("fluency", on_change=lambda:[not_change_session(True)])
relevance = st.sidebar.toggle("relevance", on_change=lambda:[not_change_session(True)])


st.sidebar.write("---")
add = st.sidebar.button("register source")

observe_session()

_layer = st.session_state.layer
_source = st.session_state.source
_level = st.session_state.menu
_title = st.session_state.title
_sum = st.session_state.summary
_change = st.session_state.not_change
_reg = st.session_state.reg


time.sleep(0.1)

# print(_reg)

if add or _reg:
  reg_session(True)
  add_source_text()
elif _level == "Level 1":
  # print(f"Level 1: {_layer} {_title}, {_source}")
  # print(f"Not Change: {_change}")

  st.empty()
  if _layer==0:
    layer_0(1)
  elif _layer==1:
    layer_1(_title, _source)
  elif _layer==2:
    layer_2(_title, _source, _sum)

elif _level == "Level 2":
  st.empty()
  # print(f"Level 2: {_layer} {_title}, {_source}")
  # print(f"Not Change: {_change}")
  if _layer==0:
    layer_0(2)
  elif _layer==1:
    layer_1(_title, _source)