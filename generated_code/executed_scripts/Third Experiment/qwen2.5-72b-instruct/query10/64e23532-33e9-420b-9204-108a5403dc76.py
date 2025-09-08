import os
import csv
import json

root_dir = "root_dir"

def process_media_views(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        account_views = {}
        for media_type in ["posts", "reels", "stories"]:
            media_dir = os.path.join(root_dir, "media", media_type)
            if not os.path.exists(media_dir):
                continue

            for year_month in os.listdir(media_dir):
                year_month_dir = os.path.join(media_dir, year_month)
                if not os.path.isdir(year_month_dir):
                    continue

                for file_name in os.listdir(year_month_dir):
                    file_path = os.path.join(year_month_dir, file_name)
                    if not file_name.endswith(".json"):
                        continue

                    with open(file_path, 'r') as file:
                        try:
                            data = json.load(file)
                            for entry in data.get("media_list_data", []):
                                account = entry.get("string_map_data", {}).get("Account", {}).get("value", "Unknown")
                                post_views = entry.get("string_map_data", {}).get("Post Views", {}).get("value", 0)
                                video_views = entry.get("string_map_data", {}).get("Video Views", {}).get("value", 0)

                                if account not in account_views:
                                    account_views[account] = {"Post Views": 0, "Video Views": 0}
                                account_views[account]["Post Views"] += post_views
                                account_views[account]["Video Views"] += video_views
                        except json.JSONDecodeError:
                            raise ValueError("Error: Failed to decode JSON file.")

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account, views in account_views.items():
                writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

    except Exception as e:
        print(f"Error: {str(e)}")

process_media_views(root_dir)