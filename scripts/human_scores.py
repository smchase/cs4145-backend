from quality_control import aggregate_scores
import json
from urllib.request import urlopen


file_path = "../data/prolific-responses.json"
url_string = "https://cs4145-api-726011437905.europe-west4.run.app/questions"
data_path = "../data/dataset.json"


with urlopen(url_string) as url:
    id_data = json.load(url)
with open(file_path, "r", encoding="utf-8") as data_file:
    human_data = json.load(data_file)
with open(data_path, "r", encoding="utf-8") as og_file:
    dataset = json.load(og_file)

question_dict = {}
for entry in human_data:
    current_id = entry["question_id"]
    current_faithfulness = 1.0 if entry["is_faithful"] else 0.0
    current_relevancy = 1.0 if entry["is_relevant"] else 0.0

    if current_id not in question_dict:
        current_question_unit = list(filter(lambda q: q["id"] == current_id, id_data))
        assert len(current_question_unit) == 1, "More than one matching ID!"
        current_question = current_question_unit[0]

        labeled_question_unit = list(
            filter(
                lambda q: q["query"] == current_question["query"]
                and q["response"] == current_question["response"],
                dataset,
            )
        )
        assert len(labeled_question_unit) == 1, "More than 1 matching ID!"
        labeled_question = labeled_question_unit[0]

        question_dict[current_id] = {
            "query": current_question["query"],
            "response": current_question["response"],
            "measured_faithfulness": labeled_question["faithfulness"],
            "measured_relevancy": labeled_question["relevancy"],
            "f_inputs": [(current_faithfulness, entry["faithfulness"])],
            "r_inputs": [(current_relevancy, entry["relevance"])],
        }
    else:
        question_dict[current_id]["f_inputs"].append(
            (current_faithfulness, entry["faithfulness"])
        )
        question_dict[current_id]["r_inputs"].append(
            (current_relevancy, entry["relevance"])
        )

for q_id in question_dict:
    perceived_faithfulness, f_rationales, perceived_relevancy, r_rationales = (
        aggregate_scores(
            question_dict[q_id]["f_inputs"], question_dict[q_id]["r_inputs"]
        )
    )
    question_dict[q_id].update(
        {
            "perceived_faithfulness": perceived_faithfulness,
            "perceived_relevancy": perceived_relevancy,
            "f_rationales": f_rationales,
            "r_rationales": r_rationales,
        }
    )

with open("../data/results.json", "w", encoding="utf-8") as output_file:
    json.dump(question_dict, output_file, indent=4)
