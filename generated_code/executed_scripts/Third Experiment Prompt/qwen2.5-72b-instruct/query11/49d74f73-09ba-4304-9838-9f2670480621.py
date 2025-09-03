import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

def get_viewed_accounts(posts_viewed_file):
    try:
        data = load_json_file(posts_viewed_file)
        viewed_accounts = set()
        for entry in data.get("impressions_history_posts_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                viewed_accounts.add(author)
        return viewed_accounts
    except Exception as e:
        print(f"Error processing posts_viewed.json: {e}")
        return set()

def get_liked_accounts(liked_posts_file):
    try:
        data = load_json_file(liked_posts_file)
        liked_accounts = set()
        for entry in data.get("likes_media_likes", []):
            for item in entry.get("string_list_data", []):
                account = item.get("value")
                if account:
                    liked_accounts.add(account)
        return liked_accounts
    except Exception as e:
        print(f"Error processing liked_posts.json: {e}")
        return set()

def find_accounts_viewed_but_not_liked(root_dir):
    posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    viewed_accounts = get_viewed_accounts(posts_viewed_file) if os.path.exists(posts_viewed_file) else set()
    liked_accounts = get_liked_accounts(liked_posts_file) if os.path.exists(liked_posts_file) else set()

    accounts_viewed_but_not_liked = viewed_accounts - liked_accounts

    return accounts_viewed_but_not_liked

def save_to_csv(accounts, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

try:
    accounts_viewed_but_not_liked = find_accounts_viewed_but_not_liked(root_dir)
    save_to_csv(accounts_viewed_but_not_liked, 'query_responses/results.csv')
except Exception as e:
    print(f"Error: {e}")
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])