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
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if "ads_information" in data and "ads_viewed.json" in data["ads_information"]:
                # Extract the accounts from the JSON data
                for account in data["ads_information"]["ads_viewed.json"]["structure"]["impressions_history_ads_seen"]:
                    accounts.append(account["string_map_data"]["Author"]["value"])

            # Check if the JSON data contains the required information
            if "ads_information" in data and "posts_viewed.json" in data["ads_information"]:
                # Extract the accounts from the JSON data
                for account in data["ads_information"]["posts_viewed.json"]["structure"]["impressions_history_posts_seen"]:
                    accounts.append(account["string_map_data"]["Author"]["value"])

            # Check if the JSON data contains the required information
            if "ads_information" in data and "videos_watched.json" in data["ads_information"]:
                # Extract the accounts from the JSON data
                for account in data["ads_information"]["videos_watched.json"]["structure"]["impressions_history_videos_watched"]:
                    accounts.append(account["string_map_data"]["Author"]["value"])

# Write the accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account"])  # Write the header
    for account in accounts:
        writer.writerow([account])