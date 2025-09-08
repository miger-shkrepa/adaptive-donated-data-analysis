import os
import csv
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            import json
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract ads information from the JSON content
def extract_ads_information(json_content):
    ads_info = defaultdict(int)
    if 'impressions_history_posts_seen' in json_content:
        for entry in json_content['impressions_history_posts_seen']:
            if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                author = entry['string_map_data']['Author']['value']
                ads_info[author] += 1
    return ads_info

# Main function to process the directory and generate the CSV
def generate_ads_csv(root_dir):
    # Define the path to the posts_viewed.json file
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    
    # Check if the file exists
    if not os.path.exists(posts_viewed_path):
        # If the file does not exist, create an empty CSV with headers
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        return
    
    # Read the JSON file
    json_content = read_json_file(posts_viewed_path)
    
    # Extract ads information
    ads_info = extract_ads_information(json_content)
    
    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, count in ads_info.items():
            writer.writerow([company, count])

# Ensure the output directory exists
os.makedirs('query_responses', exist_ok=True)

# Generate the CSV
generate_ads_csv(root_dir)