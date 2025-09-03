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
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

# Function to extract topics of interest from the JSON structure
def extract_topics_of_interest(json_data):
    topics = []
    try:
        label_values = json_data.get("label_values", [])
        for item in label_values:
            if "vec" in item:
                for value in item["vec"]:
                    topics.append(value["value"])
            elif "value" in item:
                topics.append(item["value"])
    except (AttributeError, KeyError):
        raise ValueError("Error: Failed to extract topics of interest from the JSON structure.")
    return topics

# Main function to process the directory and generate the CSV file
def process_directory():
    try:
        topics_of_interest = []

        # Construct the path to the JSON file containing topics of interest
        topics_file_path = os.path.join(root_dir, "personal_information", "information_about_you", "locations_of_interest.json")

        if os.path.exists(topics_file_path):
            json_data = read_json_file(topics_file_path)
            topics_of_interest = extract_topics_of_interest(json_data)

        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])  # Write the header
            for topic in topics_of_interest:
                writer.writerow([topic])

    except FileNotFoundError as e:
        print(e)
        # If the file does not exist, create an empty CSV with only the header
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
    except ValueError as e:
        print(e)
        # If there is an error in processing, create an empty CSV with only the header
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Execute the main function
process_directory()