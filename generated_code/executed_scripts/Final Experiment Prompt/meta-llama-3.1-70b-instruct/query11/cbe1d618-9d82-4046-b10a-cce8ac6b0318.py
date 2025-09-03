import json
import csv
import os

root_dir = "root_dir"

def get_viewed_accounts(root_dir):
    viewed_accounts = set()
    posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if os.path.exists(posts_viewed_file):
        with open(posts_viewed_file, "r") as f:
            data = json.load(f)
            for post in data.get("impressions_history_posts_seen", []):
                author = post.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    viewed_accounts.add(author)
    return viewed_accounts

def get_liked_accounts(root_dir):
    liked_accounts = set()
    liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    if os.path.exists(liked_posts_file):
        with open(liked_posts_file, "r") as f:
            data = json.load(f)
            for post in data.get("likes_media_likes", []):
                title = post.get("title")
                if title:
                    liked_accounts.add(title)
    return liked_accounts

def get_accounts_viewed_but_not_liked(root_dir):
    viewed_accounts = get_viewed_accounts(root_dir)
    liked_accounts = get_liked_accounts(root_dir)
    accounts_viewed_but_not_liked = viewed_accounts - liked_accounts
    return accounts_viewed_but_not_liked

def save_to_csv(accounts, output_file):
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        accounts_viewed_but_not_liked = get_accounts_viewed_but_not_liked(root_dir)
        output_file = "query_responses/results.csv"
        save_to_csv(accounts_viewed_but_not_liked, output_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except ValueError as e:
        raise ValueError(f"ValueError: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")

if __name__ == "__main__":
    main()