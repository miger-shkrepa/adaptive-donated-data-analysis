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

# Function to extract data from a JSON file
def extract_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        data = json.load(f)
    return data.get("structure", {}).get("impressions_history_ads_seen", [])

# Extract data from the JSON files
ads_viewed_data = extract_data(ads_viewed_path)
videos_watched_data = extract_data(videos_watched_path)

# Combine the data and count the views per account
views_per_account = {}
for data in [ads_viewed_data, videos_watched_data]:
    for item in data:
        account = item.get("string_map_data", {}).get("Author", {}).get("value", "")
        if account:
            if account not in views_per_account:
                views_per_account[account] = {"Post Views": 0, "Video Views": 0}
            if "ads_viewed" in file_path:
                views_per_account[account]["Post Views"] += 1
            elif "videos_watched" in file_path:
                views_per_account[account]["Video Views"] += 1

# Convert the data to a list of dictionaries
for account, views in views_per_account.items():
    results.append({"Account": account, "Post Views": views["Post Views"], "Video Views": views["Video Views"]})

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Account", "Post Views", "Video Views"])
    writer.writeheader()
    writer.writerows(results)