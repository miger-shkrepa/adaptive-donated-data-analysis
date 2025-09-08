import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Iterate over the JSON files in the 'your_instagram_activity' directory
for file in os.listdir(root_dir):
    if file.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, file), 'r') as f:
            # Load the JSON data
            data = eval(f.read())

            # Check if the file contains 'likes' and 'saved' data
            if 'likes' in data and 'saved' in data:
                # Iterate over the 'likes' data
                for post in data['likes']['liked_posts.json']['structure']['likes_media_likes']:
                    # Check if the post has a 'title' and a 'string_list_data'
                    if 'title' in post and 'string_list_data' in post:
                        # Iterate over the 'string_list_data'
                        for item in post['string_list_data']:
                            # Check if the item has a 'href' and a 'value'
                            if 'href' in item and 'value' in item:
                                # Check if the 'value' is not 'liked'
                                if item['value'] != 'liked':
                                    # Get the account from the 'href'
                                    account = item['href'].split('/')[-1]

                                    # Add the account to the list
                                    accounts.append(account)

                # Iterate over the 'saved' data
                for post in data['saved']['saved_posts.json']['structure']['saved_saved_media']:
                    # Check if the post has a 'title' and a 'string_map_data'
                    if 'title' in post and 'string_map_data' in post:
                        # Check if the 'string_map_data' has a 'Saved on' key
                        if 'Saved on' in post['string_map_data']:
                            # Get the account from the 'href'
                            account = post['string_map_data']['Saved on']['href'].split('/')[-1]

                            # Check if the account is not already in the list
                            if account not in accounts:
                                # Add the account to the list
                                accounts.append(account)

# Write the accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Account'])  # Write the header
    writer.writerows([[account] for account in accounts])  # Write the accounts