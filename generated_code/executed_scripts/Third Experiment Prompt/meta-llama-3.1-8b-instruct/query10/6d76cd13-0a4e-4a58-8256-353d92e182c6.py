import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Iterate over the directory structure
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'posts_viewed.json':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        if 'structure' in data and 'impressions_history_posts_seen' in data['structure']:
                            for item in data['structure']['impressions_history_posts_seen']:
                                if 'string_map_data' in item and 'Author' in item['string_map_data']:
                                    account = item['string_map_data']['Author']['value']
                                    post_views = 1
                                    video_views = 0
                                    writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})
                        else:
                            print(f"Warning: File '{file_path}' does not contain the expected structure. Skipping...")
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found.")
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON in file '{file_path}'.")
            elif file == 'reels.json':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        if 'structure' in data and 'ig_reels_media' in data['structure']:
                            for item in data['structure']['ig_reels_media']:
                                if item and 'media' in item:
                                    account = item[0]['title']
                                    post_views = 0
                                    video_views = 1
                                    writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})
                        else:
                            print(f"Warning: File '{file_path}' does not contain the expected structure. Skipping...")
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found.")
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON in file '{file_path}'.")
            elif file == 'stories.json':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        if 'structure' in data and 'ig_stories' in data['structure']:
                            for item in data['structure']['ig_stories']:
                                if item and 'media_metadata' in item:
                                    account = item['title']
                                    post_views = 0
                                    video_views = 1
                                    writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})
                        else:
                            print(f"Warning: File '{file_path}' does not contain the expected structure. Skipping...")
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found.")
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON in file '{file_path}'.")
            elif file == 'posts_1.json':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        if 'structure' in data:
                            for item in data['structure']:
                                if item and 'media' in item:
                                    account = item['title']
                                    post_views = 1
                                    video_views = 0
                                    writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})
                        else:
                            print(f"Warning: File '{file_path}' does not contain the expected structure. Skipping...")
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found.")
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON in file '{file_path}'.")