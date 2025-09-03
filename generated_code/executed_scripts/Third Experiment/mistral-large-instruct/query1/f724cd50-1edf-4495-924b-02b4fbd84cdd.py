import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract topics of interest from ad_preferences.json
def extract_topics_of_interest(root_dir):
    topics_of_interest = set()

    # Path to the ad_preferences.json file
    ad_preferences_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'ad_preferences.json')

    # Check if the file exists
    if not os.path.exists(ad_preferences_path):
        raise FileNotFoundError("FileNotFoundError: The ad_preferences.json file does not exist.")

    # Read the ad_preferences.json file
    try:
        with open(ad_preferences_path, 'r') as file:
            data = json.load(file)
            for item in data.get('label_values', []):
                if isinstance(item, dict):
                    for sub_item in item.get('dict', []):
                        if isinstance(sub_item, dict):
                            for sub_sub_item in sub_item.get('dict', []):
                                if isinstance(sub_sub_item, dict):
                                    topics_of_interest.add(sub_sub_item.get('value', ''))
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ad_preferences.json file is not a valid JSON.")

    return topics_of_interest

# Function to write topics of interest to a CSV file
def write_topics_to_csv(topics_of_interest, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

# Main function to execute the script
def main():
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Extract topics of interest
    try:
        topics_of_interest = extract_topics_of_interest(root_dir)
    except Exception as e:
        # If an error occurs, write only the column headers to the CSV
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
        raise e

    # Write the topics of interest to the CSV file
    write_topics_to_csv(topics_of_interest, output_csv)

if __name__ == "__main__":
    main()