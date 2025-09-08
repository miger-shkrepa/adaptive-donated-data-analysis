import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")

def get_viewed_accounts(posts_viewed_file):
    try:
        data = load_json_data(posts_viewed_file)
        viewed_accounts = set()
        for entry in data.get("impressions_history_posts_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                viewed_accounts.add(author)
        return viewed_accounts
    except Exception as e:
        print(f"Error processing viewed posts: {e}")
        return set()

def get_liked_accounts(liked_posts_file):
    try:
        data = load_json_data(liked_posts_file)
        liked_accounts = set()
        for entry in data.get("likes_media_likes", []):
            for item in entry.get("string_list_data", []):
                account = item.get("value")
                if account:
                    liked_accounts.add(account)
        return liked_accounts
    except Exception as e:
        print(f"Error processing liked posts: {e}")
        return set()

def find_accounts_viewed_not_liked(root_dir):
    try:
        posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

        viewed_accounts = get_viewed_accounts(posts_viewed_file) if os.path.exists(posts_viewed_file) else set()
        liked_accounts = get_liked_accounts(liked_posts_file) if os.path.exists(liked_posts_file) else set()

        accounts_viewed_not_liked = viewed_accounts - liked_accounts

        return accounts_viewed_not_liked
    except Exception as e:
        print(f"Error: {e}")
        return set()

def save_to_csv(accounts, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        accounts_viewed_not_liked = find_accounts_viewed_not_liked(root_dir)
        save_to_csv(accounts_viewed_not_liked, 'query_responses/results.csv')
    except Exception as e:
        print(f"Error: {e}")