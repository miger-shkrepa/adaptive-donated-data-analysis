import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the directory structure
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    if "your_instagram_activity" in data:
                        for key, value in data["your_instagram_activity"].items():
                            if key == "content":
                                for subkey, subvalue in value.items():
                                    if subkey == "archived_posts.json":
                                        for item in subvalue["ig_archived_post_media"]:
                                            if "cross_post_source" in item["media_metadata"]:
                                                company_names.append(item["media_metadata"]["cross_post_source"]["source_app"])
                                    elif subkey == "posts_1.json":
                                        for item in subvalue:
                                            if "cross_post_source" in item["media"]:
                                                company_names.append(item["media"][0]["cross_post_source"]["source_app"])
                                    elif subkey == "profile_photos.json":
                                        for item in subvalue["ig_profile_picture"]:
                                            if "cross_post_source" in item["media_metadata"]:
                                                company_names.append(item["media_metadata"]["cross_post_source"]["source_app"])
                                    elif subkey == "recently_deleted_content.json":
                                        for item in subvalue["ig_recently_deleted_media"]:
                                            if "cross_post_source" in item["media"]:
                                                company_names.append(item["media"][0]["cross_post_source"]["source_app"])
                                    elif subkey == "reels.json":
                                        for item in subvalue["ig_reels_media"]:
                                            if "cross_post_source" in item["media"]:
                                                company_names.append(item["media"][0]["cross_post_source"]["source_app"])
                                    elif subkey == "stories.json":
                                        for item in subvalue["ig_stories"]:
                                            if "cross_post_source" in item["media_metadata"]:
                                                company_names.append(item["media_metadata"]["cross_post_source"]["source_app"])
            except json.JSONDecodeError:
                print(f"Error parsing JSON file: {file_path}")

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    writer.writerows([[company] for company in company_names])