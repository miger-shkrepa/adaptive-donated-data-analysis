import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Define the paths to the JSON files
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Process the liked_posts.json file
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, 'r') as f:
        data = json.load(f)
        for post in data["likes_media_likes"]:
            for item in post["string_list_data"]:
                # Extract the company name from the href field
                # This assumes that the company name is the first part of the URL, before the first '/'
                company_name = item["href"].split('/')[0]
                if company_name not in company_names:
                    company_names.append(company_name)

# Process the saved_posts.json file
if os.path.exists(saved_posts_path):
    with open(saved_posts_path, 'r') as f:
        data = json.load(f)
        for post in data["saved_saved_media"]:
            for key, value in post["string_map_data"]["Saved on"].items():
                if key == "href":
                    # Extract the company name from the href field
                    # This assumes that the company name is the first part of the URL, before the first '/'
                    company_name = value.split('/')[0]
                    if company_name not in company_names:
                        company_names.append(company_name)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name"])
    for name in company_names:
        writer.writerow([name])