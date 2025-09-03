import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize data structures to store the results
account_views = {}

# Function to process JSON files
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to count views from a JSON file
def count_views(file_path, view_type):
    data = process_json_file(file_path)
    for entry in data.get(view_type, []):
        author = entry.get('string_map_data', {}).get('Author', {}).get('value', 'Unknown')
        if author not in account_views:
            account_views[author] = {'Post Views': 0, 'Video Views': 0}
        account_views[author][view_type] += 1

# Process posts_viewed.json
posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
try:
    count_views(posts_viewed_path, 'Post Views')
except Exception as e:
    print(e)

# Process videos_watched.json
videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
try:
    count_views(videos_watched_path, 'Video Views')
except Exception as e:
    print(e)

# Write the results to a CSV file
try:
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in account_views.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})
except Exception as e:
    raise IOError(f"Error: IOError: Failed to write to the CSV file {output_csv}. {str(e)}")

print(f"Results have been written to {output_csv}")