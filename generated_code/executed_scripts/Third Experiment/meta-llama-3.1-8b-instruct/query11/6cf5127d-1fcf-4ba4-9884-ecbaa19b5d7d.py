import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Check if the JSON data contains the required information
            if "impressions_history_posts_seen" in data and "likes_comment_likes" in data:
                # Extract the accounts from the JSON data
                accounts.extend([account["value"] for account in eval(data)["impressions_history_posts_seen"][0]["string_map_data"]["Author"]])
                accounts.extend([account["value"] for account in eval(data)["likes_comment_likes"][0]["string_list_data"]])
            elif "impressions_history_posts_seen" in data:
                # Extract the accounts from the JSON data
                accounts.extend([account["value"] for account in eval(data)["impressions_history_posts_seen"][0]["string_map_data"]["Author"]])
            elif "likes_comment_likes" in data:
                # Extract the accounts from the JSON data
                accounts.extend([account["value"] for account in eval(data)["likes_comment_likes"][0]["string_list_data"]])

# Remove duplicates from the list of accounts
accounts = list(set(accounts))

# Write the accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the header
    writer.writerows([[account] for account in accounts])  # Write the accounts