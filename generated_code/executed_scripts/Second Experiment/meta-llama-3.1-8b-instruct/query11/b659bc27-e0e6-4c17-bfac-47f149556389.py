import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the account names
accounts = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            
            # Check if the file contains the required data
            if "impressions_history_posts_seen" in data and "impressions_history_posts_liked" in data:
                # Extract the account names from the JSON data
                seen_accounts = [item["string_map_data"]["Author"]["value"] for item in data["impressions_history_posts_seen"]]
                liked_accounts = [item["string_map_data"]["Author"]["value"] for item in data["impressions_history_posts_liked"]]
                
                # Find the accounts that have viewed posts but not liked them
                accounts.extend([account for account in seen_accounts if account not in liked_accounts])

# Write the account names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the header
    writer.writerows([[account] for account in accounts])