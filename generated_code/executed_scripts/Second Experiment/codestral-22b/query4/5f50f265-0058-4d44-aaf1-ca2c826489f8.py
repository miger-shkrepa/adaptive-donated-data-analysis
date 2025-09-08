import os
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store company names
companies = []

# Define the JSON files that may contain information about companies
json_files = ["avatar_items.json", "reels_comments.json", "event_reminders.json", "liked_posts.json"]

# Iterate over the JSON files
for json_file in json_files:
    file_path = os.path.join(root_dir, "your_instagram_activity", json_file)

    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

            # Extract company names based on the structure of each file
            if json_file == "avatar_items.json":
                for item in data["ig_avatar_marketplace_avatar_items"]:
                    if "company" in item:
                        companies.append(item["company"])
            elif json_file == "reels_comments.json":
                for comment in data["comments_reels_comments"]:
                    if "Media Owner" in comment["string_map_data"]:
                        companies.append(comment["string_map_data"]["Media Owner"]["value"])
            elif json_file == "event_reminders.json":
                for event in data["events_event_reminders"]:
                    for string_data in event["string_list_data"]:
                        if "value" in string_data and string_data["value"] not in companies:
                            companies.append(string_data["value"])
            elif json_file == "liked_posts.json":
                for post in data["likes_media_likes"]:
                    for string_data in post["string_list_data"]:
                        if "value" in string_data and string_data["value"] not in companies:
                            companies.append(string_data["value"])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name"])
    for company in set(companies):
        writer.writerow([company])