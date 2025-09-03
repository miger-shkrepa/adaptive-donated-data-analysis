import os
import json
import csv
from collections import Counter

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

# Initialize a counter for interactions
interactions = Counter()

# Define the JSON files to be processed
files = ["post_likes.json", "story_likes.json", "comments.json"]

# Process each file
for file in files:
    file_path = os.path.join(root_dir, "logged_information", "activity", file)
    # If the file does not exist, skip it
    if not os.path.exists(file_path):
        continue
    with open(file_path, "r") as f:
        data = json.load(f)
        for item in data:
            user = item.get("title", "")
            interactions[user] += 1

# Get the top 20 users
top_users = interactions.most_common(20)

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Interactions"])
    for user, count in top_users:
        writer.writerow([user, count])