import csv
import os

def get_post_views(root_dir):
    post_views = 0
    for filename in os.listdir(root_dir):
        if filename == "posts_viewed.json":
            with open(os.path.join(root_dir, filename), 'r') as f:
                data = eval(f.read())
                for impression in data["impressions_history_posts_seen"]:
                    post_views += 1
    return post_views

def get_video_views(root_dir):
    video_views = 0
    for filename in os.listdir(root_dir):
        if filename == "videos_watched.json":
            with open(os.path.join(root_dir, filename), 'r') as f:
                data = eval(f.read())
                for impression in data["impressions_history_videos_watched"]:
                    video_views += 1
    return video_views

def get_account_names(root_dir):
    account_names = set()
    for filename in os.listdir(root_dir):
        if filename == "ads_and_topics.json":
            with open(os.path.join(root_dir, filename), 'r') as f:
                data = eval(f.read())
                for ad in data["ads_viewed.json"]["impressions_history_ads_seen"]:
                    account_names.add(ad["string_map_data"]["Author"]["value"])
                for post in data["posts_viewed.json"]["impressions_history_posts_seen"]:
                    account_names.add(post["string_map_data"]["Author"]["value"])
                for video in data["videos_watched.json"]["impressions_history_videos_watched"]:
                    account_names.add(video["string_map_data"]["Author"]["value"])
    return account_names

def main():
    root_dir = "root_dir"
    try:
        root_dir = os.path.dirname(root_dir)
    except NameError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    post_views = get_post_views(root_dir)
    video_views = get_video_views(root_dir)
    account_names = get_account_names(root_dir)
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])
        for account in account_names:
            writer.writerow([account, post_views if account in [post["string_map_data"]["Author"]["value"] for post in get_post_views(root_dir)] else 0, video_views if account in [video["string_map_data"]["Author"]["value"] for video in get_video_views(root_dir)] else 0])

if __name__ == "__main__":
    main()