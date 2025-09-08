import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def process_liked_posts(data):
    post_views = 0
    video_views = 0
    accounts = set()
    for item in data.get("likes_media_likes", []):
        for string_data in item.get("string_list_data", []):
            accounts.add(string_data.get("value", ""))
            if "post" in string_data.get("value", "").lower():
                post_views += 1
            elif "video" in string_data.get("value", "").lower():
                video_views += 1
    return accounts, post_views, video_views

def process_saved_posts(data):
    post_views = 0
    video_views = 0
    accounts = set()
    for item in data.get("saved_saved_media", []):
        title = item.get("title", "")
        accounts.add(title)
        if "post" in title.lower():
            post_views += 1
        elif "video" in title.lower():
            video_views += 1
    return accounts, post_views, video_views

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

        liked_posts_data = {}
        saved_posts_data = {}

        if os.path.exists(liked_posts_path):
            liked_posts_data = load_json(liked_posts_path)
        if os.path.exists(saved_posts_path):
            saved_posts_data = load_json(saved_posts_path)

        liked_accounts, liked_post_views, liked_video_views = process_liked_posts(liked_posts_data)
        saved_accounts, saved_post_views, saved_video_views = process_saved_posts(saved_posts_data)

        all_accounts = liked_accounts.union(saved_accounts)
        account_views = {account: {"Post Views": 0, "Video Views": 0} for account in all_accounts}

        for account in liked_accounts:
            account_views[account]["Post Views"] += liked_post_views
            account_views[account]["Video Views"] += liked_video_views

        for account in saved_accounts:
            account_views[account]["Post Views"] += saved_post_views
            account_views[account]["Video Views"] += saved_video_views

        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account, views in account_views.items():
                writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()