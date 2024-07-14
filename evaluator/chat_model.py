from openai import AzureOpenAI
from typing import TypeVar
from typing import List, Callable, Union
from utils import get_num_tokens
from tenacity import retry
from tenacity import stop_after_delay, RetryError, wait_fixed, stop_after_attempt

Self = TypeVar("Self", bound="Chat_Model")

class Chat_Model():
  def __init__(
      self: Self, 
      api_key: str, api_version: str, endpoint:str,
      model_name: str, deploy_name: str
      ) -> None:
    self.client = AzureOpenAI(
      api_key = api_key,
      api_version = api_version,
      azure_endpoint = endpoint
    )
    self.model_name = model_name
    self.deploy_name = deploy_name
  
  @staticmethod
  def create_messages(system_prompt: str, user_prompt: str, fewshot_samples: List[dict]) -> List[dict]:
    messages = []
    messages.append({"role": "system", "content": system_prompt})
    if len(fewshot_samples) > 0:
      messages.append(fewshot_samples)
    messages.append({"role": "user", "content": user_prompt})
    return messages

  # @retry(stop=(stop_after_attempt(5) | stop_after_delay(600)), wait=wait_fixed(2))
  def get_response(
      self: Self,
      system_prompt: str, user_prompt: str, 
      gpt_parameters: dict, parse_response : Callable, 
      fewshot_samples: List[dict] = [], max_input_tokens: int = 5000,
      ) -> Union[dict, str]:
    
    messages = self.create_messages(system_prompt, user_prompt, fewshot_samples)

    num_tokens = get_num_tokens(self.model_name, messages)

    while num_tokens > max_input_tokens:
      print(f"Draft tokens: {num_tokens} > {max_input_tokens}.")
      reduce_tokens_by = num_tokens - max_input_tokens
      messages[-1] = {"role": "user", "content": messages[:-reduce_tokens_by]}

    response = self.client.chat.completions.create(
      **gpt_parameters,
      model=self.deploy_name,
      messages=messages
    )

    response = parse_response(response)

    return response