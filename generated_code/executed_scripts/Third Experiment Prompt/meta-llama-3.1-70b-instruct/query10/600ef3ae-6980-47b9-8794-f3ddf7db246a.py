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

        # Iterate through 'your_instagram_activity' directory
        activity_dir = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(activity_dir):
            return account_views

        # Iterate through 'likes' directory
        likes_dir = os.path.join(activity_dir, "likes")
        if not os.path.exists(likes_dir):
            return account_views

        # Open 'liked_posts.json' file
        liked_posts_file = os.path.join(likes_dir, "liked_posts.json")
        if not os.path.exists(liked_posts_file):
            return account_views

        with open(liked_posts_file, "r") as f:
            liked_posts_data = json.load(f)

        # Extract account views from 'liked_posts.json'
        for post in liked_posts_data["likes_media_likes"]:
            account = post["title"]
            if account not in account_views:
                account_views[account] = 0
            account_views[account] += 1

        # Iterate through 'saved' directory
        saved_dir = os.path.join(activity_dir, "saved")
        if not os.path.exists(saved_dir):
            return account_views

        # Open 'saved_posts.json' file
        saved_posts_file = os.path.join(saved_dir, "saved_posts.json")
        if not os.path.exists(saved_posts_file):
            return account_views

        with open(saved_posts_file, "r") as f:
            saved_posts_data = json.load(f)

        # Extract account views from 'saved_posts.json'
        for post in saved_posts_data["saved_saved_media"]:
            account = post["title"]
            if account not in account_views:
                account_views[account] = 0
            account_views[account] += 1

    except FileNotFoundError as e:
        raise e
    except json.JSONDecodeError as e:
        raise ValueError("Error: Invalid JSON format in file.")
    except Exception as e:
        raise ValueError("Error: An unexpected error occurred.")

    return account_views

def write_csv(account_views):
    csv_file = "query_responses/results.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Account", "Post Views", "Video Views"])
        for account, views in account_views.items():
            writer.writerow([account, views, 0])  # Video views are not available in the data

account_views = get_account_views(root_dir)
write_csv(account_views)