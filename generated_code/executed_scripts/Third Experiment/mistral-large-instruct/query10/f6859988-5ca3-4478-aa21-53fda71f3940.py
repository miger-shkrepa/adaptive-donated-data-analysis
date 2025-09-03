import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize data structures to store the results
account_views = {}

# Function to process JSON files and extract relevant data
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to process posts viewed data
def process_posts_viewed(file_path):
    data = process_json_file(file_path)
    for entry in data.get('impressions_history_posts_seen', []):
        author = entry.get('string_map_data', {}).get('Author', {}).get('value', '')
        if author:
            if author not in account_views:
                account_views[author] = {'Post Views': 0, 'Video Views': 0}
            account_views[author]['Post Views'] += 1

# Function to process videos watched data
def process_videos_watched(file_path):
    data = process_json_file(file_path)
    for entry in data.get('impressions_history_videos_watched', []):
        author = entry.get('string_map_data', {}).get('Author', {}).get('value', '')
        if author:
            if author not in account_views:
                account_views[author] = {'Post Views': 0, 'Video Views': 0}
            account_views[author]['Video Views'] += 1

# Main function to process the directory structure
def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Process posts viewed data
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if os.path.exists(posts_viewed_path):
            process_posts_viewed(posts_viewed_path)

        # Process videos watched data
        videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
        if os.path.exists(videos_watched_path):
            process_videos_watched(videos_watched_path)

        # Write the results to the CSV file
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account, views in account_views.items():
                writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

    except Exception as e:
        print(f"Error: {e}")

# Run the main function
if __name__ == "__main__":
    main()