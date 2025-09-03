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
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for post in data["impressions_history_posts_seen"]:
                            author = post["string_map_data"]["Author"]["value"]
                            if author not in views:
                                views[author] = 0
                            views[author] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file 'posts_viewed.json' does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file 'posts_viewed.json' is not a valid JSON file.")
            elif filename == "videos_watched.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for video in data["impressions_history_videos_watched"]:
                            author = video["string_map_data"]["Author"]["value"]
                            if author not in views:
                                views[author] = 0
                            views[author] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file 'videos_watched.json' does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file 'videos_watched.json' is not a valid JSON file.")
    return views

def write_to_csv(views):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])
        for account, view_count in views.items():
            writer.writerow([account, view_count, 0])

def main():
    try:
        views = get_views(root_dir)
        write_to_csv(views)
    except FileNotFoundError as e:
        print(e)
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account", "Post Views", "Video Views"])
    except ValueError as e:
        print(e)
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account", "Post Views", "Video Views"])

if __name__ == "__main__":
    main()