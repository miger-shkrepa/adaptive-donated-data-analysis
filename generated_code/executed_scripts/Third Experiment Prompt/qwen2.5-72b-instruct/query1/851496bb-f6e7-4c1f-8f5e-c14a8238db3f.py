import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

# Function to extract topics of interest from the JSON structure
def extract_topics_of_interest(json_data):
    topics = []
    try:
        label_values = json_data.get("label_values", [])
        for item in label_values:
            label = item.get("label")
            if label == "Topics of Interest":
                vec = item.get("vec", [])
                for value in vec:
                    topics.append(value.get("value"))
    except (AttributeError, KeyError):
        pass  # Handle missing or unexpected structure gracefully
    return topics

# Main function to process the directory and generate the CSV file
def process_directory():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        topics_of_interest = []

        # Path to the JSON file containing topics of interest
        topics_file_path = os.path.join(root_dir, "personal_information", "information_about_you", "locations_of_interest.json")
        
        if os.path.exists(topics_file_path):
            json_data = read_json_file(topics_file_path)
            topics_of_interest.extend(extract_topics_of_interest(json_data))

        # Write the results to a CSV file
        output_file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])  # Write the header
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        print(f"An error occurred: {e}")

# Execute the main function
process_directory()