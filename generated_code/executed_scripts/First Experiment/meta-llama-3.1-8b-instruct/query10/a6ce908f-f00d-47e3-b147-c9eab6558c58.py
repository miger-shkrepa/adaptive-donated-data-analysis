import csv
import os

# Define the root directory variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the data structures
account_views = {}
video_views = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)

            # Iterate over the data
            for item in data:
                # Check if the item is a post or video view
                if item['type'] == 'json' and 'impressions_history_ads_seen' in item['structure']:
                    # Increment the post view count for the account
                    account = item['structure']['impressions_history_ads_seen'][0]['string_map_data']['Author']['value']
                    if account not in account_views:
                        account_views[account] = 0
                    account_views[account] += 1
                elif item['type'] == 'json' and 'impressions_history_videos_watched' in item['structure']:
                    # Increment the video view count for the account
                    account = item['structure']['impressions_history_videos_watched'][0]['string_map_data']['Author']['value']
                    if account not in video_views:
                        video_views[account] = 0
                    video_views[account] += 1

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for account, views in account_views.items():
        writer.writerow({'Account': account, 'Post Views': views, 'Video Views': video_views.get(account, 0)})