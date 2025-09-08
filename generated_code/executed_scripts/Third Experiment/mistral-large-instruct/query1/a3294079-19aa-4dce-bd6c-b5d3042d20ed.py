import os
import json
import csv

def extract_topics_of_interest(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    topics_of_interest = set()

    # Define the path to the relevant JSON file
    topics_file_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'other_categories_used_to_reach_you.json')

    # Check if the file exists
    if not os.path.exists(topics_file_path):
        raise FileNotFoundError("Error: The file 'other_categories_used_to_reach_you.json' does not exist.")

    # Read the JSON file
    try:
        with open(topics_file_path, 'r') as file:
            data = json.load(file)
            if 'label_values' in data:
                for item in data['label_values']:
                    if 'label' in item and 'vec' in item:
                        for vec_item in item['vec']:
                            if 'value' in vec_item:
                                topics_of_interest.add(vec_item['value'])
    except json.JSONDecodeError:
        raise ValueError("Error: The file 'other_categories_used_to_reach_you.json' is not a valid JSON file.")

    # Create the output directory if it does not exist
    output_dir = 'query_responses'
    os.makedirs(output_dir, exist_ok=True)

    # Write the results to a CSV file
    output_file_path = os.path.join(output_dir, 'results.csv')
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
        for topic in topics_of_interest:
            writer.writerow([topic])

if __name__ == "__main__":
    root_dir = "root_dir"
    extract_topics_of_interest(root_dir)