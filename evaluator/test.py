from evaluator.evaluator import run
import sys
import krippendorff
import yaml
import pandas as pd

def test(cfg, system_prompt, user_prompt, criteria, targets):
  source_texts = targets["source_text"]
  student_summaries = targets["student_summary"]
  answer_scores = targets["score"].to_list()
  scores = []
  for idx in range(targets.shape[0]):
    source_text = source_texts[idx]
    student_summary = student_summaries[idx]
    response = run(cfg, source_text, system_prompt, user_prompt, criteria, student_summary)
    scores.append(response["rating"])
  
  reliability_data = [answer_scores, scores]
  return krippendorff.alpha(reliability_data=reliability_data, level_of_measurement="ordinal")

if __name__ == "__main__":
  args = sys.argv
  type = args[0]
  data_path = args[1]
  if type == "gpt35":
    with open("/home/work/evaluator/configs/gpt3_5.yaml", "r") as f:
      config = yaml.safe_load(f)
  else:
    with open("/home/work/evaluator/configs/gpt4.yaml", "r") as f:
      config = yaml.safe_load(f)
  criterias = ["coherence", "consistency", "fluency", "relevance"]

  with open("/home/work/evaluator/prompt/system_prompt.txt", "r") as f:
    system_prompt = f.read()

  with open("/home/work/evaluator/prompt/user_prompt.txt", "r") as f:
    user_prompt = f.read()

  targets = pd.read_csv(data_path)

  peformances = {}

  for criteria in criterias:
    peformances[criteria] = test(config, system_prompt, user_prompt, criteria, targets)

  print(peformances)