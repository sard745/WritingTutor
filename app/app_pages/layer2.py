import streamlit as st
from components.back_btn import back_btn

# criterias = ["coherence", "consistency", "fluency", "relevance"]

def layer_2(title, source, input, items):
  st.write(title)
  col1, col2 = st.columns(2)
  with open(source, "r") as f:
      s_text = f.read()

  col1.text_area(
            ":black[Source text]",
            value=f'{s_text}',
            height=400,
        )

  col2.text_area(
            "Summary", 
            value=input,
            height=400,
        )
  
  st.write("---")
  st.write("Feedback")
  for item in items:
    if st.session_state[f"feedback_{item}"] is not None:
      st.markdown(f"- {item.capitalize()}: {st.session_state[f'feedback_{item}']['rating']}  \n{st.session_state[f'feedback_{item}']['analysis']}")
  back_btn()