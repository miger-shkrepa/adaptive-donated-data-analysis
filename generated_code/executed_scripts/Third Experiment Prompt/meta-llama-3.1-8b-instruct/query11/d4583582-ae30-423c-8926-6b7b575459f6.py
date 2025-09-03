import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the account IDs
accounts = []

# Iterate over the subdirectories in the root directory
for dir_name, dir_contents, _ in os.walk(root_dir):
    # Check if the subdirectory is 'ads_information'
    if dir_name == os.path.join(root_dir, 'ads_information'):
        # Iterate over the subdirectories in 'ads_information'
        for sub_dir_name, sub_dir_contents, _ in os.walk(dir_name):
            # Check if the subdirectory is 'ads_and_topics'
            if sub_dir_name == os.path.join(dir_name, 'ads_and_topics'):
                # Iterate over the files in 'ads_and_topics'
                for file_name in sub_dir_contents:
                    # Check if the file is 'posts_viewed.json'
                    if file_name == 'posts_viewed.json':
                        # Open the file and read its contents
                        with open(os.path.join(sub_dir_name, file_name), 'r') as file:
                            data = file.read()
                            # Parse the JSON data
                            import json
                            data = json.loads(data)
                            # Extract the account IDs from the JSON data
                            for item in data['structure']['impressions_history_posts_seen']:
                                account_id = item['string_map_data']['Author']['value']
                                accounts.append(account_id)

                    # Check if the file is 'liked_posts.json'
                    elif file_name == 'liked_posts.json':
                        # Open the file and read its contents
                        with open(os.path.join(sub_dir_name, file_name), 'r') as file:
                            data = file.read()
                            # Parse the JSON data
                            import json
                            data = json.loads(data)
                            # Extract the account IDs from the JSON data
                            for item in data['structure']['likes_media_likes']:
                                account_id = item['string_list_data'][0]['value']
                                accounts.append(account_id)

# Write the account IDs to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account'])  # Write the header
    for account in accounts:
        writer.writerow([account])