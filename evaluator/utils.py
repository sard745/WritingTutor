import tiktoken
import json

def make_prompt(
    prompt: str, criteria: str,
    source_text: str, student_summary: str
    ) -> dict:
    
  system_prompt = prompt.replace(
    "$evaluation_criteria", criteria["evaluation_criteria"]
    )
  system_prompt = system_prompt.replace(
    "$evaluation_step", criteria["evaluation_step"]
    )
  system_prompt = system_prompt.replace(
    "$question", criteria["question"]
    )
  system_prompt = system_prompt.replace(
    "$source_text", source_text
    )
  
  tag_start = "<student-summary>"
  tag_end = "</student-summary>"
  user_prompt = student_summary.strip()
  user_prompt = tag_start + user_prompt + tag_end

  return dict(
    system_prompt = system_prompt,
    user_prompt = student_summary
  ) 

def get_num_tokens(
      model_name: str, messages: str
      ) -> int:
    # TODO: tiktokenに定義されていないモデルの場合の処理を追加する
    encoding = tiktoken.encoding_for_model(model_name)

    if model_name in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4o-0513"
    }:
      tokens_per_message = 3
      tokens_per_name = 1
    elif model_name == "gpt-3.5-turbo":
      tokens_per_message = 4
      tokens_per_name = -1
    else:
      raise NotImplementedError(
        f"""get_num_tokens_from_messages() not implemented for model {model_name}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
      )

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>

    return num_tokens

# TODO: api料金を簡単に計算できる関数を追加する