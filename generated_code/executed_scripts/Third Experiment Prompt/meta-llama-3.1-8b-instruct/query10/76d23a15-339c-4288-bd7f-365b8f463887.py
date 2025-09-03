import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Iterate over the 'ads_information' directory
    for account in os.listdir(os.path.join(root_dir, "ads_information")):
        account_dir = os.path.join(root_dir, "ads_information", account)
        if os.path.isdir(account_dir):
            post_views = 0
            video_views = 0

            # Iterate over the 'ads_and_topics' directory
            for file in os.listdir(account_dir):
                file_path = os.path.join(account_dir, file)
                if file.endswith(".json"):
                    try:
                        with open(file_path, 'r') as json_file:
                            data = json.load(json_file)
                            if isinstance(data, dict) and 'type' in data:
                                if 'impressions_history_ads_seen' in data.get('structure', {}):
                                    post_views += len(data['structure']['impressions_history_ads_seen'])
                                if 'impressions_history_videos_watched' in data.get('structure', {}):
                                    video_views += len(data['structure']['impressions_history_videos_watched'])
                            else:
                                print(f"Skipping file {file_path} because it's not a JSON object or doesn't have a 'type' key.")
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON in file {file_path}: {e}")

            # Write the account and view counts to the CSV file
            writer.writerow([account, post_views, video_views])