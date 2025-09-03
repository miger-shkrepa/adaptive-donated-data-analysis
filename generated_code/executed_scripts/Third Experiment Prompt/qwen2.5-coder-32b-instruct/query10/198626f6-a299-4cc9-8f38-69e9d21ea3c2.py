import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files safely
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Initialize a dictionary to store account views
account_views = {}

# Function to process posts viewed
def process_posts_viewed(file_path):
    try:
        data = read_json_file(file_path)
        for entry in data.get('impressions_history_posts_seen', []):
            author = entry['string_map_data'].get('Author', {}).get('value', 'Unknown')
            if author not in account_views:
                account_views[author] = {'Post Views': 0, 'Video Views': 0}
            account_views[author]['Post Views'] += 1
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Function to process videos watched
def process_videos_watched(file_path):
    try:
        data = read_json_file(file_path)
        for entry in data.get('impressions_history_videos_watched', []):
            author = entry['string_map_data'].get('Author', {}).get('value', 'Unknown')
            if author not in account_views:
                account_views[author] = {'Post Views': 0, 'Video Views': 0}
            account_views[author]['Video Views'] += 1
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Process posts_viewed.json
posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
if os.path.exists(posts_viewed_path):
    process_posts_viewed(posts_viewed_path)

# Process videos_watched.json
videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
if os.path.exists(videos_watched_path):
    process_videos_watched(videos_watched_path)

# Prepare the CSV output
output_path = 'query_responses/results.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for account, views in account_views.items():
        writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

print(f"Results saved to {output_path}")