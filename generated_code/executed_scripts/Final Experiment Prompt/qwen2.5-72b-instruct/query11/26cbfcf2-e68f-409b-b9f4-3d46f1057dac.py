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

def get_viewed_accounts(data):
    viewed_accounts = set()
    for entry in data.get("impressions_history_posts_seen", []):
        author = entry.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            viewed_accounts.add(author)
    return viewed_accounts

def get_liked_accounts(data):
    liked_accounts = set()
    for entry in data.get("likes_media_likes", []):
        title = entry.get("title")
        if title:
            liked_accounts.add(title)
    return liked_accounts

def find_accounts_viewed_not_liked(viewed_accounts, liked_accounts):
    return viewed_accounts - liked_accounts

def save_to_csv(accounts, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])
        for account in accounts:
            writer.writerow([account])

def main():
    try:
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

        posts_viewed_data = {}
        liked_posts_data = {}

        if os.path.exists(posts_viewed_path):
            posts_viewed_data = load_json_data(posts_viewed_path)
        else:
            print("Warning: posts_viewed.json not found. Assuming no posts were viewed.")

        if os.path.exists(liked_posts_path):
            liked_posts_data = load_json_data(liked_posts_path)
        else:
            print("Warning: liked_posts.json not found. Assuming no posts were liked.")

        viewed_accounts = get_viewed_accounts(posts_viewed_data)
        liked_accounts = get_liked_accounts(liked_posts_data)

        accounts_viewed_not_liked = find_accounts_viewed_not_liked(viewed_accounts, liked_accounts)

        save_to_csv(accounts_viewed_not_liked, 'query_responses/results.csv')

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()