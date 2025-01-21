import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

file_path = "data\prolific-responses.json"

# Load data from JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

correct_answer = {
    "id": "96e9c8a6-2c8d-44a4-928e-c61b9fa68f88",
    "is_faithful": True,
    "is_relevant": True,
    "keywords": ["waste products", "blood pressure", "balance"],
    "response": "The kidneys filter waste products and excess fluids from the blood, maintain electrolyte balance, regulate blood pressure, and remove toxins from the body."
}

def calculate_time_differences(data):
    worker_times = {}

    for entry in data:
        worker_id = entry["worker_id"]
        time_value = datetime.fromisoformat(entry["time"])
        
        if worker_id not in worker_times:
            worker_times[worker_id] = []

        worker_times[worker_id].append(time_value)

    time_differences = {}

    for worker_id, times in worker_times.items():
        min_time = min(times)
        max_time = max(times)
        diff_minutes = (max_time - min_time).total_seconds() / 60
        time_differences[worker_id] = diff_minutes

    return time_differences


def check_correctness(data, correct_answer):
    correctness = {}

    for entry in data:
        if entry["question_id"] == correct_answer["id"]:
            worker_id = entry["worker_id"]
            keywords_matched = any(
                keyword in entry["faithfulness"] or keyword in entry["relevance"]
                for keyword in correct_answer["keywords"]
            )

            if keywords_matched and entry["is_faithful"] == correct_answer["is_faithful"] and entry["is_relevant"] == correct_answer["is_relevant"]:
                correctness[worker_id] = True
            else:
                correctness[worker_id] = False

    return correctness

# Compute time differences and correctness
worker_time_differences = calculate_time_differences(data)
def create_boxplot(time_differences):
    times = list(time_differences.values())

    plt.figure(figsize=(6, 8))  # Adjust dimensions for vertical orientation
    box = plt.boxplot(times, vert=True, patch_artist=True, boxprops=dict(facecolor="lightblue"))

    # Enable grid and add horizontal grid lines
    plt.grid(axis="y", linestyle="--", color="gray", alpha=0.7)

    # Add title and labels
    plt.title("Task Duration")
    plt.ylabel("Time (minutes)")
    plt.xticks([])  # Customize X-axis to show label for the box plot
    plt.show()

create_boxplot(worker_time_differences)

worker_correctness = check_correctness(data, correct_answer)
def create_correctness_table(correctness):
    correct_count = sum(correctness.values())
    incorrect_count = len(correctness) - correct_count

    print("Correctness Summary:")
    print(f"Correct Answers: {correct_count}")
    print(f"Incorrect Answers: {incorrect_count}")

create_correctness_table(worker_correctness)
def create_time_range_table(time_differences):
    times = np.array(list(time_differences.values()))
    mean_time = np.mean(times)
    std_dev_time = np.std(times)
    ranges = {
        "0-10 minutes": 0,
        "10-20 minutes": 0,
        "20-30 minutes": 0,
        ">30 minutes": 0,
    }

    for time in time_differences.values():
        if 0 <= time <= 10:
            ranges["0-10 minutes"] += 1
        elif 10 < time <= 20:
            ranges["10-20 minutes"] += 1
        elif 20 < time <= 30:
            ranges["20-30 minutes"] += 1
        elif time > 30: 
            ranges[">30 minutes"] += 1

    print("Time Ranges Summary:")
    for range_label, count in ranges.items():
        print(f"{range_label}: {count} workers")
    print(f"Mean Time: {mean_time:.2f} minutes")
    print(f"Standard Deviation: {std_dev_time:.2f} minutes")

create_time_range_table(worker_time_differences)
# Output results
print("Time Differences (in minutes):", worker_time_differences)
print("Correctness for specific question:", worker_correctness)