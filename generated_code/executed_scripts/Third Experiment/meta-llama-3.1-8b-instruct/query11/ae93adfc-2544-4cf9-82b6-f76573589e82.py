import csv
import os

# Declare the variable referring to the file input
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
            # Check if the JSON data contains the required structure
            if "impressions_history_posts_seen" in data and "likes_comment_likes" in data:
                # Extract the accounts from the JSON data
                posts_seen = [item["string_map_data"]["Author"]["value"] for item in eval(data)["structure"]["impressions_history_posts_seen"]]
                likes = [item["string_list_data"][0]["value"] for item in eval(data)["structure"]["likes_comment_likes"]]
                # Add the accounts to the list
                accounts.extend([account for account in posts_seen if account not in likes])

# Write the accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the column headers
    writer.writerows([[account] for account in accounts])  # Write the accounts