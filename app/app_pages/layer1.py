import streamlit as st
from session_state import layer_session
from components.back_btn import back_btn

import yaml
import json
import os
import sys
sys.path.append(os.getcwd())
from evaluator import evaluator

# criterias = ["coherence", "consistency", "fluency", "relevance"]

def layer_1(title, path, criterias):
  st.write(title)
  with open(path, "r") as f:
    s_text = f.read()

  col1, col2 = st.columns(2)
  with st.form("form"):
    col1, col2 = st.columns(2)

    with col1:
      st.text_area(
                  ":black[Source text]",
                  value=f'{s_text}',
                  height=400,
              )
      
    with col2:
      st.text_area(
                  "Summary", 
                  key = "summary",
                  height=400,
              )
      
    st.form_submit_button("submit", on_click=lambda:[evaluate(s_text, st.session_state.summary, criterias), layer_session(2)])
  
  back_btn()

def evaluate(source, summary, items):
  if st.session_state.model == "gpt-3.5":
    with open("/home/work/evaluator/configs/gpt3_5.yaml", "r") as f:
      config = yaml.safe_load(f)
  else:
    with open("/home/work/evaluator/configs/gpt4.yaml", "r") as f:
      config = yaml.safe_load(f)

  with open("/home/work/evaluator/prompt/system_prompt.txt", "r") as f:
    system_prompt = f.read()

  with open("/home/work/evaluator/prompt/user_prompt.txt", "r") as f:
    user_prompt = f.read()

  for item in items:
    if st.session_state[item]:
      with open(f"/home/work/evaluator/prompt/criteria/{item}.json", "r") as f:
        criteria = json.load(f)
      feedback = evaluator.run(config, source, system_prompt, user_prompt, criteria, summary)
      st.session_state[f"feedback_{item}"] = feedback
    else:
      st.session_state[f"feedback_{item}"] = None