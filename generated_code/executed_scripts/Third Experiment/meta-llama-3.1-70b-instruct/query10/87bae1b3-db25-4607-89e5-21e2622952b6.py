import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("Error: The 'ads_and_topics' directory does not exist.")
        
        posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
        videos_watched_file = os.path.join(ads_and_topics_dir, "videos_watched.json")
        
        if os.path.exists(posts_viewed_file):
            with open(posts_viewed_file, 'r') as file:
                posts_viewed_data = json.load(file)
                for post in posts_viewed_data["impressions_history_posts_seen"]:
                    author = post["string_map_data"]["Author"]["value"]
                    if author not in account_views:
                        account_views[author] = {"post_views": 1, "video_views": 0}
                    else:
                        account_views[author]["post_views"] += 1
        
        if os.path.exists(videos_watched_file):
            with open(videos_watched_file, 'r') as file:
                videos_watched_data = json.load(file)
                for video in videos_watched_data["impressions_history_videos_watched"]:
                    author = video["string_map_data"]["Author"]["value"]
                    if author not in account_views:
                        account_views[author] = {"post_views": 0, "video_views": 1}
                    else:
                        account_views[author]["video_views"] += 1
        
        return account_views
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: Failed to parse JSON - {e}")
    except Exception as e:
        raise ValueError(f"Error: An error occurred - {e}")

def save_to_csv(account_views):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Post Views", "Video Views"])
            for account, views in account_views.items():
                writer.writerow([account, views["post_views"], views["video_views"]])
    
    except Exception as e:
        raise ValueError(f"Error: Failed to save to CSV - {e}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        account_views = get_account_views(root_dir)
        if not account_views:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Account", "Post Views", "Video Views"])
        else:
            save_to_csv(account_views)
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: An error occurred - {e}")

if __name__ == "__main__":
    main()