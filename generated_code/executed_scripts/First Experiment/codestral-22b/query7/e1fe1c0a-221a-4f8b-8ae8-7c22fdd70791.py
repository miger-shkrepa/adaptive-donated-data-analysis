import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement count for each user
engagement_count = {}

# Traverse the directory structure
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "instagram_profile_information.json":
            file_path = os.path.join(foldername, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                for item in data["profile_account_insights"]:
                    if "First Story Time" in item["string_map_data"]:
                        user = item["title"]
                        if user in engagement_count:
                            engagement_count[user] += 1
                        else:
                            engagement_count[user] = 1

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, count in engagement_count.items():
        writer.writerow([user, count])