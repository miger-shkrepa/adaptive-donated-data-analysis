import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")

        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            posts_viewed_data = []
        else:
            with open(posts_viewed_file, 'r') as f:
                posts_viewed_data = json.load(f)["impressions_history_posts_seen"]

        videos_watched_file = os.path.join(ads_and_topics_dir, "videos_watched.json")
        if not os.path.exists(videos_watched_file):
            videos_watched_data = []
        else:
            with open(videos_watched_file, 'r') as f:
                videos_watched_data = json.load(f)["impressions_history_videos_watched"]

        for post in posts_viewed_data:
            author = post["string_map_data"]["Author"]["value"]
            if author not in account_views:
                account_views[author] = {"Post Views": 0, "Video Views": 0}
            account_views[author]["Post Views"] += 1

        for video in videos_watched_data:
            author = video["string_map_data"]["Author"]["value"]
            if author not in account_views:
                account_views[author] = {"Post Views": 0, "Video Views": 0}
            account_views[author]["Video Views"] += 1

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError:
        raise ValueError("ValueError: Invalid JSON format.")

    except Exception as e:
        raise ValueError(f"ValueError: {e}")

    return account_views

def save_to_csv(account_views):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for account, views in account_views.items():
                writer.writerow({"Account": account, "Post Views": views["Post Views"], "Video Views": views["Video Views"]})

    except Exception as e:
        raise ValueError(f"ValueError: {e}")

def main():
    try:
        account_views = get_account_views(root_dir)
        save_to_csv(account_views)

    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise ValueError(f"ValueError: {e}")

if __name__ == "__main__":
    main()