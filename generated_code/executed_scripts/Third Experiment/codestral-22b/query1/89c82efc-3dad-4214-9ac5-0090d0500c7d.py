import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

topics_of_interest = []

ads_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
if os.path.exists(ads_dir):
    ads_viewed_file = os.path.join(ads_dir, "ads_viewed.json")
    if os.path.exists(ads_viewed_file):
        with open(ads_viewed_file, 'r') as f:
            data = json.load(f)
            for ad in data["impressions_history_ads_seen"]:
                if "Author" in ad["string_map_data"]:
                    topics_of_interest.append(ad["string_map_data"]["Author"]["value"])

    posts_viewed_file = os.path.join(ads_dir, "posts_viewed.json")
    if os.path.exists(posts_viewed_file):
        with open(posts_viewed_file, 'r') as f:
            data = json.load(f)
            for post in data["impressions_history_posts_seen"]:
                if "Author" in post["string_map_data"]:
                    topics_of_interest.append(post["string_map_data"]["Author"]["value"])

    videos_watched_file = os.path.join(ads_dir, "videos_watched.json")
    if os.path.exists(videos_watched_file):
        with open(videos_watched_file, 'r') as f:
            data = json.load(f)
            for video in data["impressions_history_videos_watched"]:
                if "Author" in video["string_map_data"]:
                    topics_of_interest.append(video["string_map_data"]["Author"]["value"])

with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])