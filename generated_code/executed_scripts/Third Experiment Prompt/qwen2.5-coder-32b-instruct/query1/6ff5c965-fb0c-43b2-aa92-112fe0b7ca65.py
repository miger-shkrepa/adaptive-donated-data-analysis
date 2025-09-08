import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the ads_viewed.json file
ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

# Initialize a set to store unique topics of interest
topics_of_interest = set()

# Function to extract topics from the ads_viewed.json file
def extract_topics_from_ads_viewed(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'impressions_history_ads_seen' in data:
                for entry in data['impressions_history_ads_seen']:
                    if 'string_map_data' in entry:
                        for key, value in entry['string_map_data'].items():
                            if key == 'Topics':
                                if isinstance(value, dict) and 'value' in value:
                                    topics_of_interest.add(value['value'])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the ads_viewed.json file: {str(e)}")

# Check if the ads_viewed.json file exists and extract topics
if os.path.exists(ads_viewed_path):
    extract_topics_from_ads_viewed(ads_viewed_path)

# Define the path for the output CSV file
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the topics of interest to the CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Topics of Interest'])
    for topic in topics_of_interest:
        csvwriter.writerow([topic])

print(f"Results have been saved to {output_csv_path}")