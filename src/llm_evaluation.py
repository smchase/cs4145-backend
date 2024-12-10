import json
from llama_index.llms.openai import OpenAI
from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator


data_path = "../data/query-response-pairs.json"
measured_scores_path = "../data/measured-scores.json"


data = {}
with open(data_path, "r") as data_file:
    try:
        data = json.load(data_file)
    except json.JSONDecodeError as e:
        print("Could not read JSON file:", e)

llm = OpenAI(model="gpt-4-turbo", temperature=0.0)
faithfulness_evaluator = FaithfulnessEvaluator(llm)
relevancy_evaluator = RelevancyEvaluator(llm)

output_list = []
count = 0
for query, response_data in data.items():
    response_text = response_data["response_text"]
    for source_node in response_data["source_nodes"]:
        current_object = {}
        context = source_node["node_content"]

        faithfulness_result = faithfulness_evaluator.evaluate(query, response_text, [context])
        relevancy_result = relevancy_evaluator.evaluate(query, response_text, [context])

        current_object["query"] = query
        current_object["response"] = response_text
        current_object["context"] = context
        current_object["faithfulness_result"] = str(faithfulness_result.passing)
        current_object["faithfulness_score"] = faithfulness_result.score
        current_object["faithfulness_feedback"] = faithfulness_result.feedback
        current_object["relevancy_result"] = str(relevancy_result.passing)
        current_object["relevancy_score"] = relevancy_result.score
        current_object["relevancy_feedback"] = relevancy_result.feedback

        output_list.append(current_object)
    count += 1

    # Stop after the first 20 data instances (just looking into how much each model charges)
    if count == 10:
        break

with open(measured_scores_path, "w") as output_file:
    json.dump(output_list, output_file, indent=4)
