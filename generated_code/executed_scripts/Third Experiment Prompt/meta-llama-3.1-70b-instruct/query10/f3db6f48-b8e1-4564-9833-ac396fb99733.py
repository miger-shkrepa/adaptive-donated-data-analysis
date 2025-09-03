import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        # Get posts views
        posts_views_file = os.path.join(root_dir, "your_activity_across_facebook", "messages", "inbox", "posts_viewed.json")
        if os.path.exists(posts_views_file):
            with open(posts_views_file, 'r') as f:
                posts_views_data = json.load(f)
                for post in posts_views_data["impressions_history_posts_seen"]:
                    account = post["string_map_data"]["Author"]["value"]
                    if account not in account_views:
                        account_views[account] = {"Post Views": 0, "Video Views": 0}
                    account_views[account]["Post Views"] += 1
        else:
            print("Warning: posts_viewed.json not found. Assuming 0 post views.")

        # Get videos views
        videos_views_file = os.path.join(root_dir, "your_activity_across_facebook", "messages", "inbox", "videos_watched.json")
        if os.path.exists(videos_views_file):
            with open(videos_views_file, 'r') as f:
                videos_views_data = json.load(f)
                for video in videos_views_data["impressions_history_videos_watched"]:
                    account = video["string_map_data"]["Author"]["value"]
                    if account not in account_views:
                        account_views[account] = {"Post Views": 0, "Video Views": 0}
                    account_views[account]["Video Views"] += 1
        else:
            print("Warning: videos_watched.json not found. Assuming 0 video views.")

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError("Error: Invalid JSON format in file. " + str(e))
    except Exception as e:
        raise Exception("Error: An unexpected error occurred. " + str(e))

    return account_views

def save_to_csv(account_views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ["Account", "Post Views", "Video Views"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in account_views.items():
            writer.writerow({"Account": account, "Post Views": views["Post Views"], "Video Views": views["Video Views"]})

def main():
    account_views = get_account_views(root_dir)
    save_to_csv(account_views)

if __name__ == "__main__":
    main()