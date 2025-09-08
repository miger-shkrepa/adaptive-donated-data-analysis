import os
import csv
import json

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store company names
company_names = []

# Define the JSON files that may contain information about companies
json_files = [
    "your_instagram_activity/avatars_store/avatar_items.json",
    "your_instagram_activity/comments/reels_comments.json",
    "your_instagram_activity/events/event_reminders.json",
    "your_instagram_activity/likes/liked_posts.json"
]

# Iterate over the JSON files
for json_file in json_files:
    file_path = os.path.join(root_dir, json_file)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {json_file} does not exist.")

    # Load the JSON data
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract the company names from the JSON data
    # This is a placeholder and may need to be adjusted based on the actual structure of the JSON files
    for item in data:
        if 'string_map_data' in item and 'Media Owner' in item['string_map_data']:
            company_names.append(item['string_map_data']['Media Owner']['value'])

# Remove duplicates from the company names list
company_names = list(set(company_names))

# Save the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Company Name'])
    for company_name in company_names:
        writer.writerow([company_name])