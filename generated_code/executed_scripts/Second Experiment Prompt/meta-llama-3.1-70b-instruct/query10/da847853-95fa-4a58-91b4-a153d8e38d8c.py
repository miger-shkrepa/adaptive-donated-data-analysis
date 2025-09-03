import os
import json
import csv

root_dir = "root_dir"

def get_views(root_dir):
    views = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "posts_viewed.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if "impressions_history_posts_seen" in data:
                            for post in data["impressions_history_posts_seen"]:
                                if "string_map_data" in post and "Author" in post["string_map_data"]:
                                    author = post["string_map_data"]["Author"]["value"]
                                    if author not in views:
                                        views[author] = {"Post Views": 0, "Video Views": 0}
                                    views[author]["Post Views"] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file 'posts_viewed.json' does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file 'posts_viewed.json' is not a valid JSON file.")
            elif filename == "videos_watched.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if "impressions_history_videos_watched" in data:
                            for video in data["impressions_history_videos_watched"]:
                                if "string_map_data" in video and "Author" in video["string_map_data"]:
                                    author = video["string_map_data"]["Author"]["value"]
                                    if author not in views:
                                        views[author] = {"Post Views": 0, "Video Views": 0}
                                    views[author]["Video Views"] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file 'videos_watched.json' does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file 'videos_watched.json' is not a valid JSON file.")
    return views

def write_to_csv(views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views_count in views.items():
            writer.writerow({'Account': account, 'Post Views': views_count["Post Views"], 'Video Views': views_count["Video Views"]})

def main():
    try:
        views = get_views(root_dir)
        if not views:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Account', 'Post Views', 'Video Views']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        else:
            write_to_csv(views)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()