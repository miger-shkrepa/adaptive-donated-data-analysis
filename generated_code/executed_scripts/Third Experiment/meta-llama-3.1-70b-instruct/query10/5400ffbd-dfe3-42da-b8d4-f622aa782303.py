import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate over ads_and_topics directory
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if os.path.exists(ads_and_topics_dir):
            for filename in os.listdir(ads_and_topics_dir):
                if filename == "posts_viewed.json":
                    posts_viewed_path = os.path.join(ads_and_topics_dir, filename)
                    with open(posts_viewed_path, "r") as file:
                        posts_viewed_data = json.load(file)
                        for post in posts_viewed_data["impressions_history_posts_seen"]:
                            author = post["string_map_data"]["Author"]["value"]
                            if author not in account_views:
                                account_views[author] = {"Post Views": 0, "Video Views": 0}
                            account_views[author]["Post Views"] += 1

                elif filename == "videos_watched.json":
                    videos_watched_path = os.path.join(ads_and_topics_dir, filename)
                    with open(videos_watched_path, "r") as file:
                        videos_watched_data = json.load(file)
                        for video in videos_watched_data["impressions_history_videos_watched"]:
                            author = video["string_map_data"]["Author"]["value"]
                            if author not in account_views:
                                account_views[author] = {"Post Views": 0, "Video Views": 0}
                            account_views[author]["Video Views"] += 1

        # If no data is available, return empty dictionary
        if not account_views:
            return {}

        return account_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_views):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Post Views", "Video Views"])
            for account, views in account_views.items():
                writer.writerow([account, views["Post Views"], views["Video Views"]])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    account_views = get_account_views(root_dir)
    if not account_views:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Post Views", "Video Views"])
    else:
        save_to_csv(account_views)

if __name__ == "__main__":
    main()