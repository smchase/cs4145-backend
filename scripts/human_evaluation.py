import json

file_path = "data\\results.json"

# Function to process the JSON data
def process_json_file(file_path):
    # Open the file and load the data into a dictionary
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Dictionary to store the result
    result_dict = {}
    
    # Initialize sum counters for relevance and faithfulness
    total_relevance = 0
    total_faithfulness = 0
    count = 0

    # Iterate through each key-value pair in the JSON data
    for key, value in data.items():
        # Retrieve the attributes
        measured_relevance = value.get('measured_relevancy', None)
        perceived_relevance = value.get('perceived_relevancy', None)
        measured_faithfulness = value.get('measured_faithfulness', None)
        perceived_faithfulness = value.get('perceived_faithfulness', None)
        
        # Check if measured_relevance == perceived_relevance
        relevance_result = 1 if int(float(measured_relevance)) == int(float(perceived_relevance)) else 0
        total_relevance += relevance_result
        
        # Check if measured_faithfulness == perceived_faithfulness
        faithfulness_result = 1 if int(float(measured_faithfulness)) == int(float(perceived_faithfulness)) else 0
        total_faithfulness += faithfulness_result
        
        # Store the result in the result_dict as a tuple
        result_dict[key] = (relevance_result, faithfulness_result)
        count += 1
    
    # Calculate averages
    average_relevance = total_relevance / count if count > 0 else 0
    average_faithfulness = total_faithfulness / count if count > 0 else 0
    
    return result_dict, average_relevance, average_faithfulness

# Example usage: replace 'your_file.json' with the actual path to your JSON file
result_dict, average_relevance, average_faithfulness = process_json_file(file_path)

# Print the result dictionary
print("Result Dictionary:", result_dict)

# Print the averages
print("Average Relevance:", average_relevance)
print("Average Faithfulness:", average_faithfulness)
