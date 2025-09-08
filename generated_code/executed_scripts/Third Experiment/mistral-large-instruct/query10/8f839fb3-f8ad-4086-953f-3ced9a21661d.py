import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize data collection
data = []

# Function to extract post views
def extract_post_views(directory):
    post_views = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        # Assuming post views are stored in a specific key
                        if 'post_views' in content:
                            post_views += content['post_views']
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    raise FileNotFoundError(f"Error: {e}")
    return post_views

# Function to extract video views
def extract_video_views(directory):
    video_views = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = json.load(f)
                        # Assuming video views are stored in a specific key
                        if 'video_views' in content:
                            video_views += content['video_views']
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    raise FileNotFoundError(f"Error: {e}")
    return video_views

# Function to process the directory
def process_directory(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Extract post and video views
    post_views = extract_post_views(root_dir)
    video_views = extract_video_views(root_dir)

    # Assuming the account information is stored in a specific JSON file
    account_info_path = os.path.join(root_dir, 'personal_information', 'personal_information.json')
    if os.path.exists(account_info_path):
        try:
            with open(account_info_path, 'r') as f:
                account_info = json.load(f)
                account_name = account_info['profile_user'][0]['string_map_data']['Username']['value']
                data.append([account_name, post_views, video_views])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise FileNotFoundError(f"Error: {e}")
    else:
        data.append(['Unknown', post_views, video_views])

# Process the directory
process_directory(root_dir)

# Write the results to a CSV file
try:
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account', 'Post Views', 'Video Views'])
        writer.writerows(data)
except Exception as e:
    raise FileNotFoundError(f"Error: {e}")