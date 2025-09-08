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

# Function to process a JSON file and extract the necessary data
def process_json_file(file_path):
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        data = json.load(f)

    # The structure of the JSON files is assumed to be as described in the directory structure
    # If the structure is different, this part of the code will need to be adjusted
    if "structure" in data and "impressions_history_ads_seen" in data["structure"]:
        return {item["string_map_data"]["Author"]["value"]: item["string_map_data"]["Time"]["timestamp"] for item in data["structure"]["impressions_history_ads_seen"]}
    else:
        return {}

# Process the JSON files
ads_viewed = process_json_file(ads_viewed_path)
videos_watched = process_json_file(videos_watched_path)
posts_viewed = process_json_file(posts_viewed_path)

# Combine the data from the three files
for account in set(ads_viewed.keys()).union(videos_watched.keys(), posts_viewed.keys()):
    results.append({
        "Account": account,
        "Post Views": posts_viewed.get(account, 0),
        "Video Views": videos_watched.get(account, 0)
    })

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Account", "Post Views", "Video Views"])
    writer.writeheader()
    writer.writerows(results)