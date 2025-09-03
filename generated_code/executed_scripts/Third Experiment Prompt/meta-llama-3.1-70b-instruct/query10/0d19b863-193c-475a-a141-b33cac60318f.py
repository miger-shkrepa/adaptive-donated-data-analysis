import os
import json
import csv

root_dir = "root_dir"

def get_content_views(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Initialize variables to store results
        account_views = {}

        # Iterate through ads_information directory
        ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if os.path.exists(ads_info_dir):
            for file in os.listdir(ads_info_dir):
                if file == "posts_viewed.json":
                    posts_viewed_file = os.path.join(ads_info_dir, file)
                    with open(posts_viewed_file, "r") as f:
                        posts_viewed_data = json.load(f)
                        for post in posts_viewed_data["impressions_history_posts_seen"]:
                            author = post["string_map_data"]["Author"]["value"]
                            if author not in account_views:
                                account_views[author] = {"Post Views": 0, "Video Views": 0}
                            account_views[author]["Post Views"] += 1

                elif file == "videos_watched.json":
                    videos_watched_file = os.path.join(ads_info_dir, file)
                    with open(videos_watched_file, "r") as f:
                        videos_watched_data = json.load(f)
                        for video in videos_watched_data["impressions_history_videos_watched"]:
                            author = video["string_map_data"]["Author"]["value"]
                            if author not in account_views:
                                account_views[author] = {"Post Views": 0, "Video Views": 0}
                            account_views[author]["Video Views"] += 1

        # Write results to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account, views in account_views.items():
                writer.writerow({"Account": account, "Post Views": views["Post Views"], "Video Views": views["Video Views"]})

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise ValueError("Error: An unexpected error occurred. " + str(e))

get_content_views(root_dir)