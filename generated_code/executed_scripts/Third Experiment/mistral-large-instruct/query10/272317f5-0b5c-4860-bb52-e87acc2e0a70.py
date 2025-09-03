import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize data structures to store the results
account_views = {}

# Function to process JSON files and extract data
def process_json_file(file_path, key):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for entry in data.get(key, []):
                for item in entry.get('string_list_data', []):
                    account = item.get('value', 'Unknown')
                    timestamp = item.get('timestamp', 0)
                    if account not in account_views:
                        account_views[account] = {'Post Views': 0, 'Video Views': 0}
                    account_views[account][key.split('_')[-1].capitalize() + ' Views'] += 1
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Process the posts_viewed.json file
posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
if os.path.exists(posts_viewed_path):
    process_json_file(posts_viewed_path, 'impressions_history_posts_seen')

# Process the videos_watched.json file
videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
if os.path.exists(videos_watched_path):
    process_json_file(videos_watched_path, 'impressions_history_videos_watched')

# Write the results to the CSV file
try:
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in account_views.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})
except Exception as e:
    raise IOError(f"IOError: Failed to write to the CSV file. {str(e)}")

print(f"Results have been written to {output_csv}")