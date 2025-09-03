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
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Iterate over the accounts
    for account in os.listdir(os.path.join(root_dir, 'ads_information', 'ads_and_topics')):
        if account.endswith('.json'):
            account_name = account[:-5]
            account_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', account)

            # Try to open the account file
            try:
                with open(account_path, 'r') as f:
                    data = json.load(f)

                    # Initialize the post and video views
                    post_views = 0
                    video_views = 0

                    # Check if the 'structure' key exists
                    if 'structure' in data:
                        # Iterate over the posts and videos
                        for item in data['structure']['impressions_history_recs_hidden_authors']:
                            if 'string_map_data' in item:
                                for key, value in item['string_map_data'].items():
                                    if key == 'Benutzername':
                                        post_views += 1
                                    elif key == 'Zeit':
                                        video_views += 1

                    # Write the account data to the CSV file
                    writer.writerow({'Account': account_name, 'Post Views': post_views, 'Video Views': video_views})

            # Handle missing files
            except FileNotFoundError:
                print(f"Error: File '{account_path}' not found.")
                writer.writerow({'Account': account_name, 'Post Views': 0, 'Video Views': 0})

            except json.JSONDecodeError:
                print(f"Error: File '{account_path}' is not a valid JSON file.")
                writer.writerow({'Account': account_name, 'Post Views': 0, 'Video Views': 0})

            except KeyError:
                print(f"Error: File '{account_path}' is missing the 'structure' key.")
                writer.writerow({'Account': account_name, 'Post Views': 0, 'Video Views': 0})