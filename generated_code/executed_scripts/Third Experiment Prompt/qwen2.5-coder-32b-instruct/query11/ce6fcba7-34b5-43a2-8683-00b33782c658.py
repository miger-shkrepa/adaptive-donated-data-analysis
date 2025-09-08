import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the paths to the JSON files
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

# Initialize sets to store authors
viewed_authors = set()
liked_authors = set()

# Function to read JSON file and extract authors
def extract_authors_from_json(file_path, authors_set):
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist. Skipping this file.")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'impressions_history_posts_seen' in data:
                for entry in data['impressions_history_posts_seen']:
                    if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                        authors_set.add(entry['string_map_data']['Author']['value'])
    except (FileNotFoundError, ValueError) as e:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} could not be read or parsed.") from e

# Extract authors from posts_viewed.json
extract_authors_from_json(posts_viewed_path, viewed_authors)

# Extract authors from liked_posts.json
extract_authors_from_json(liked_posts_path, liked_authors)

# Find authors that have been viewed but not liked
result_authors = viewed_authors - liked_authors

# Define the output CSV file path
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the result to a CSV file
try:
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])
        for author in result_authors:
            writer.writerow([author])
except IOError as e:
    raise IOError(f"IOError: The file {output_csv_path} could not be written.") from e