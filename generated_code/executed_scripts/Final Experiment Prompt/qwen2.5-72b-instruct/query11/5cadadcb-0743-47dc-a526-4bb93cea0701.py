import json
import csv
import os

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def extract_accounts(data, key, subkey):
    accounts = set()
    for entry in data.get(key, []):
        if subkey in entry:
            accounts.add(entry[subkey])
    return accounts

def main():
    try:
        posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

        posts_viewed_data = {}
        liked_posts_data = {}

        if os.path.exists(posts_viewed_file):
            posts_viewed_data = load_json_data(posts_viewed_file)
        if os.path.exists(liked_posts_file):
            liked_posts_data = load_json_data(liked_posts_file)

        viewed_accounts = set()
        for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                viewed_accounts.add(author)

        liked_accounts = set()
        for entry in liked_posts_data.get("likes_media_likes", []):
            title = entry.get("title")
            if title:
                liked_accounts.add(title)

        accounts_viewed_not_liked = viewed_accounts - liked_accounts

        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in accounts_viewed_not_liked:
                writer.writerow([account])

    except Exception as e:
        print(f"Error: {e}")
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

if __name__ == "__main__":
    main()