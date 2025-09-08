import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

results = []

# Define the paths to the relevant JSON files
ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Function to extract data from a JSON file
def extract_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    else:
        return []

# Extract data from the JSON files
ads_viewed_data = extract_data(ads_viewed_path)
videos_watched_data = extract_data(videos_watched_path)
posts_viewed_data = extract_data(posts_viewed_path)

# Create a dictionary to store the results
account_views = {}

# Function to update the dictionary with the data from a JSON file
def update_account_views(data, key):
    for item in data:
        if "string_map_data" in item and "Author" in item["string_map_data"]:
            account = item["string_map_data"]["Author"]["value"]
            if account not in account_views:
                account_views[account] = {"Post Views": 0, "Video Views": 0}
            account_views[account][key] += 1

# Update the dictionary with the data from the JSON files
update_account_views(ads_viewed_data, "Post Views")
update_account_views(videos_watched_data, "Video Views")
update_account_views(posts_viewed_data, "Post Views")

# Convert the dictionary to a list of lists
for account, views in account_views.items():
    results.append([account, views["Post Views"], views["Video Views"]])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Account", "Post Views", "Video Views"])
    writer.writerows(results)