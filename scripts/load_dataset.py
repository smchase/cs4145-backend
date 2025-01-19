import json
from pathlib import Path

import requests


def load_dataset():
    dataset_path = Path(__file__).parent.parent / "data" / "dataset.json"
    with open(dataset_path) as f:
        return json.load(f)


def post_question(question):
    # Transform the dataset format to match the API requirements
    data = {
        "query": question["query"],
        "context1": (
            question["context_snippets"][0]
            if len(question["context_snippets"]) > 0
            else ""
        ),
        "context2": (
            question["context_snippets"][1]
            if len(question["context_snippets"]) > 1
            else ""
        ),
        "response": question["response"],
    }

    # Send POST request to the API
    response = requests.post(
        "https://cs4145-api-726011437905.europe-west4.run.app/questions", json=data
    )

    if response.status_code == 201:
        print(f"Successfully posted question {question['id']}")
    else:
        print(f"Failed to post question {question['id']}: {response.status_code}")


def main():
    dataset = load_dataset()
    print(f"Loaded {len(dataset)} questions from dataset")

    for question in dataset:
        post_question(question)


if __name__ == "__main__":
    main()
