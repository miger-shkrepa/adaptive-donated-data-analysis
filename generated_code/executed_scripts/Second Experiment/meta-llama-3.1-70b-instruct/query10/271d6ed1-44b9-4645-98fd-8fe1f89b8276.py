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
            with open(posts_viewed_file, "r") as file:
                posts_viewed_data = json.load(file).get("impressions_history_posts_seen", [])

        videos_watched_file = os.path.join(ads_and_topics_dir, "videos_watched.json")
        if not os.path.exists(videos_watched_file):
            videos_watched_data = []
        else:
            with open(videos_watched_file, "r") as file:
                videos_watched_data = json.load(file).get("impressions_history_videos_watched", [])

        for post in posts_viewed_data:
            author = post.get("string_map_data", {}).get("Author", {}).get("value")
            if author not in account_views:
                account_views[author] = {"Post Views": 0, "Video Views": 0}
            account_views[author]["Post Views"] += 1

        for video in videos_watched_data:
            author = video.get("string_map_data", {}).get("Author", {}).get("value")
            if author not in account_views:
                account_views[author] = {"Post Views": 0, "Video Views": 0}
            account_views[author]["Video Views"] += 1

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Failed to parse JSON - {e}")

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

    return account_views

def save_to_csv(account_views):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Post Views", "Video Views"])
            for account, views in account_views.items():
                writer.writerow([account, views.get("Post Views", 0), views.get("Video Views", 0)])
    except Exception as e:
        raise ValueError(f"ValueError: Failed to save to CSV - {e}")

def main():
    try:
        account_views = get_account_views(root_dir)
        save_to_csv(account_views)
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Post Views", "Video Views"])
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

if __name__ == "__main__":
    main()