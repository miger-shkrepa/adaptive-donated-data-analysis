import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Iterate over the directory structure
    for key, value in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')).read()).items():
        if key == "impressions_history_ads_seen":
            for item in value:
                account = item.get("string_map_data", {}).get("Author", {}).get("value")
                post_views = 0
                video_views = 0
                for item2 in item.get("string_map_data", {}).items():
                    if item2[0] == "Time":
                        post_views += 1
                    elif item2[0] == "Author":
                        video_views += 1
                writer.writerow([account, post_views, video_views])

    for key, value in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')).read()).items():
        if key == "impressions_history_posts_seen":
            for item in value:
                account = item.get("string_map_data", {}).get("Author", {}).get("value")
                post_views = 0
                video_views = 0
                for item2 in item.get("string_map_data", {}).items():
                    if item2[0] == "Time":
                        post_views += 1
                    elif item2[0] == "Author":
                        video_views += 1
                writer.writerow([account, post_views, video_views])

    for key, value in json.loads(open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')).read()).items():
        if key == "impressions_history_videos_watched":
            for item in value:
                account = item.get("string_map_data", {}).get("Author", {}).get("value")
                post_views = 0
                video_views = 0
                for item2 in item.get("string_map_data", {}).items():
                    if item2[0] == "Time":
                        post_views += 1
                    elif item2[0] == "Author":
                        video_views += 1
                writer.writerow([account, post_views, video_views])