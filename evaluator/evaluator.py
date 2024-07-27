from openai.types.chat.chat_completion import ChatCompletion
import re
from evaluator.utils import make_prompt
from evaluator.chat_model import Chat_Model
import hydra
from omegaconf import DictConfig
from tenacity import retry
from tenacity import stop_after_delay, RetryError, wait_fixed, stop_after_attempt
import os
from typing import Union
from dotenv import load_dotenv

load_dotenv()

def parse_response(response: ChatCompletion) -> dict:
  content = response.choices[0].message.content

  """
  以下のすべてのパターンを抽出できるよう改良
  ・Analysis: test Score: 5
  ・Score: 5 Analysis: test
  ・Analysis: test \nScore: 5
  ・Score: 5 \nAnalysis: test
  """
  analysis_pattern = r"Analysis:\s*(.+?)(?=\s*Score:|\Z|\n)" 
  rating_pattern = r"Score:\s*(\d)"
  
  analysis = re.findall(analysis_pattern, content)
  rating = re.findall(rating_pattern, content)
  return dict(
    analysis = analysis[0],
    rating = rating[0]
  )

def evaluate(
    chat_model: Chat_Model,
    system_prompt: str, user_prompt: str,
    criteria: str, source_text: str, student_summary: str, 
    gpt_parameters: dict, max_input_tokens: int
  ) -> Union[dict,str]:

  prompts = make_prompt(system_prompt, user_prompt, criteria, source_text, student_summary)

  try:
    evaluations = chat_model.get_response(
      system_prompt=prompts["system_prompt"],
      user_prompt=prompts["user_prompt"],
      gpt_parameters=gpt_parameters,
      parse_response=parse_response,
      max_input_tokens=max_input_tokens
    )
  # 何かしらのエラーによりスコアを算出できなかった場合
  except RetryError:
    evaluations = dict(
      analysis = "We cannot caluculate score.",
      rating = 0
    )
  return evaluations

def run(cfg: dict, source_text: str, system_prompt: str, user_prompt: str, criteria: dict, student_summary: str) -> Union[dict,str]:
  gpt = cfg["gpt"]
  parameters = cfg["parameters"]
  
  chat_model = Chat_Model(
    api_key = os.getenv("AZURE_API_KEY"),
    api_version = gpt["api_version"],
    endpoint = os.getenv("AZURE_END_POINT"),
    model_name = gpt["model_name"],
    deploy_name = gpt["deploy_name"]
  )

  response = evaluate(
    chat_model = chat_model,
    system_prompt = system_prompt,
    user_prompt=user_prompt,
    criteria = criteria,
    source_text = source_text,
    student_summary = student_summary,
    gpt_parameters= parameters,
    max_input_tokens=parameters["max_tokens"]
  )

  return response
  