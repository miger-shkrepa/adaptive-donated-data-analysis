import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def get_viewed_accounts(posts_viewed_path):
    try:
        data = load_json(posts_viewed_path)
        viewed_accounts = set()
        for entry in data.get("impressions_history_posts_seen", []):
            string_map_data = entry.get("string_map_data", {})
            author = string_map_data.get("Author", {}).get("value")
            if author:
                viewed_accounts.add(author)
        return viewed_accounts
    except Exception as e:
        print(f"Error processing posts_viewed.json: {e}")
        return set()

def get_liked_accounts(liked_posts_path):
    try:
        data = load_json(liked_posts_path)
        liked_accounts = set()
        for entry in data.get("likes_media_likes", []):
            string_list_data = entry.get("string_list_data", [])
            for item in string_list_data:
                liked_accounts.add(item.get("value"))
        return liked_accounts
    except Exception as e:
        print(f"Error processing liked_posts.json: {e}")
        return set()

def find_accounts_viewed_but_not_liked(root_dir):
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

    viewed_accounts = get_viewed_accounts(posts_viewed_path)
    liked_accounts = get_liked_accounts(liked_posts_path)

    accounts_viewed_but_not_liked = viewed_accounts - liked_accounts

    return accounts_viewed_but_not_liked

def save_to_csv(accounts, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    accounts_viewed_but_not_liked = find_accounts_viewed_but_not_liked(root_dir)
    save_to_csv(accounts_viewed_but_not_liked, 'query_responses/results.csv')

if __name__ == "__main__":
    main()