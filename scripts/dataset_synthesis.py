import csv
import json

query_response_pairs = "../data/query-response-pairs.json"
measured_scores = "../data/response-metrics.csv"
dataset_path = "../data/dataset.json"


data = {}
with open(query_response_pairs, "r", encoding="utf-8") as data_file:
    try:
        data = json.load(data_file)
    except json.JSONDecodeError as e:
        print("Could not read JSON file:", e)

csv_rows = []
with open(measured_scores, "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file)
    fields = next(csv_reader)

    assert (
        "Faithfulness" == fields[-2]
    ), "No column for the measured faithfulness-score was found!"
    assert (
        "Relevancy" == fields[-1]
    ), "No column for the measured relevancy-score was found!"

    for line in csv_reader:
        csv_rows.append(line)

cross_check_queries = list(zip(data.keys(), map(lambda rs: rs[0], csv_rows)))
assert all(
    tup[0] == tup[1] for tup in cross_check_queries
), "Mismatch in the queries from the two input-files!"

cross_check_responses = list(
    zip(
        (data[key]["response_text"] for key in data.keys()),
        map(lambda rs: rs[1], csv_rows),
    )
)
assert all(
    tup[0] == tup[1] for tup in cross_check_responses
), "Mismatch in the responses from the two input-files!"

output_list = []
for idx, tup in enumerate(zip(data.items(), csv_rows)):
    query, response_data, row = tup[0][0], tup[0][1], tup[1]
    current_object = {
        "id": f"Q{idx + 1}",
        "query": query,
        "response": response_data["response_text"],
        "context_snippets": list(
            node["node_content"] for node in response_data["source_nodes"]
        ),
        "faithfulness": row[-2],
        "relevancy": row[-1],
    }
    output_list.append(current_object)

with open(dataset_path, "w", encoding="utf-8") as output_file:
    json.dump(output_list, output_file, indent=4)
