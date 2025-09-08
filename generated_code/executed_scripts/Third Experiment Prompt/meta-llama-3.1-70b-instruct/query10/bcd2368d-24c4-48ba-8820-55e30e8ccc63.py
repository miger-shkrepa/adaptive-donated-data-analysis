import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "posts_1.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for post in data:
                            for media in post["media"]:
                                account = media["title"]
                                if account not in account_views:
                                    account_views[account] = {"post_views": 0, "video_views": 0}
                                account_views[account]["post_views"] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file 'posts_1.json' does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file 'posts_1.json' is not a valid JSON file.")
            elif filename == "stories.json":
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for story in data["ig_stories"]:
                            account = story["title"]
                            if account not in account_views:
                                account_views[account] = {"post_views": 0, "video_views": 0}
                            if "video_metadata" in story["media_metadata"]:
                                account_views[account]["video_views"] += 1
                            else:
                                account_views[account]["post_views"] += 1
                except FileNotFoundError:
                    raise FileNotFoundError("Error: The file 'stories.json' does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file 'stories.json' is not a valid JSON file.")
    return account_views

def write_to_csv(account_views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in account_views.items():
            writer.writerow({"Account": account, "Post Views": views["post_views"], "Video Views": views["video_views"]})

def main():
    try:
        account_views = get_account_views(root_dir)
        write_to_csv(account_views)
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except ValueError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()