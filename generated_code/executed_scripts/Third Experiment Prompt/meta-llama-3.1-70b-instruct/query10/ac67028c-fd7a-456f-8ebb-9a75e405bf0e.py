import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "posts_viewed.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        if "impressions_history_posts_seen" in data:
                            for post in data["impressions_history_posts_seen"]:
                                if "string_map_data" in post and "Author" in post["string_map_data"]:
                                    account = post["string_map_data"]["Author"]["value"]
                                    if account not in account_views:
                                        account_views[account] = 0
                                    account_views[account] += 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    return account_views

def get_video_views(root_dir):
    video_views = {}
    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "reels.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        if "ig_reels_media" in data:
                            for reel in data["ig_reels_media"]:
                                if "media" in reel:
                                    for media in reel["media"]:
                                        if "title" in media:
                                            account = media["title"]
                                            if account not in video_views:
                                                video_views[account] = 0
                                            video_views[account] += 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    return video_views

def merge_views(account_views, video_views):
    merged_views = {}
    for account in account_views:
        merged_views[account] = {"Post Views": account_views[account], "Video Views": 0}
    for account in video_views:
        if account in merged_views:
            merged_views[account]["Video Views"] = video_views[account]
        else:
            merged_views[account] = {"Post Views": 0, "Video Views": video_views[account]}
    return merged_views

def write_csv(merged_views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in merged_views.items():
            writer.writerow({'Account': account, 'Post Views': views["Post Views"], 'Video Views': views["Video Views"]})

def main():
    account_views = get_account_views(root_dir)
    video_views = get_video_views(root_dir)
    merged_views = merge_views(account_views, video_views)
    write_csv(merged_views)

if __name__ == "__main__":
    main()