import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

account_views = {}

def process_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON file {file_path}")
        return

    if "media" in data:
        for item in data["media"]:
            if "media" in item:
                for media_item in item["media"]:
                    if "cross_post_source" in media_item and "source_app" in media_item["cross_post_source"]:
                        account = media_item["cross_post_source"]["source_app"]
                        if account not in account_views:
                            account_views[account] = {"post_views": 0, "video_views": 0}
                        if "media_metadata" in media_item and "video_metadata" in media_item["media_metadata"]:
                            account_views[account]["video_views"] += 1
                        else:
                            account_views[account]["post_views"] += 1

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.json'):
            process_json_file(os.path.join(dirpath, filename))

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for account, views in account_views.items():
        writer.writerow({'Account': account, 'Post Views': views['post_views'], 'Video Views': views['video_views']})