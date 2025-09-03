import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Iterate over the JSON files in the 'likes' directory
likes_dir = os.path.join(root_dir, "likes")
if os.path.exists(likes_dir):
    for filename in os.listdir(likes_dir):
        if filename.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(likes_dir, filename), 'r') as file:
                # Load the JSON data
                data = eval(file.read())

                # Iterate over the 'likes_media_likes' and 'likes_comment_likes' lists
                for likes_list in data['structure'].values():
                    for item in likes_list:
                        # Check if the 'string_list_data' list exists
                        if 'string_list_data' in item:
                            # Iterate over the 'string_list_data' list
                            for data_item in item['string_list_data']:
                                # Check if the 'href' key exists
                                if 'href' in data_item:
                                    # Extract the account from the 'href'
                                    account = data_item['href'].split('/')[-2]

                                    # Check if the account is not in the 'liked_posts.json' or 'liked_comments.json' file
                                    if filename == 'liked_posts.json' or filename == 'liked_comments.json':
                                        continue

                                    # Add the account to the list
                                    accounts.append(account)

# Write the accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account'])  # Write the column headers
    writer.writerows([[account] for account in accounts])  # Write the accounts