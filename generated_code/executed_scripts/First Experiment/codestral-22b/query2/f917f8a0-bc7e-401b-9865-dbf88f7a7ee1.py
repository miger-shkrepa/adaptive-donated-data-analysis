import os
import csv
import json

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the results
results = {}

# Traverse the directory structure
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "ads_viewed.json":
            file_path = os.path.join(foldername, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                for ad in data["impressions_history_ads_seen"]:
                    author = ad["string_map_data"]["Author"]["value"]
                    if author in results:
                        results[author] += 1
                    else:
                        results[author] = 1

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in results.items():
        writer.writerow([company, count])