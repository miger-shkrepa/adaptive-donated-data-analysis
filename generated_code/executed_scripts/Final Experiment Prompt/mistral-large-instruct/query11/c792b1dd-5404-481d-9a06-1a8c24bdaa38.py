import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON.")

def extract_viewed_accounts(data):
    viewed_accounts = set()
    try:
        for entry in data.get("impressions_history_posts_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                viewed_accounts.add(author)
    except (TypeError, AttributeError) as e:
        raise ValueError(f"Error: ValueError: {e}")
    return viewed_accounts

def extract_liked_accounts(data):
    liked_accounts = set()
    try:
        for entry in data.get("likes_media_likes", []):
            title = entry.get("title")
            if title:
                liked_accounts.add(title)
    except (TypeError, AttributeError) as e:
        raise ValueError(f"Error: ValueError: {e}")
    return liked_accounts

def main():
    viewed_posts_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

    viewed_accounts = set()
    liked_accounts = set()

    try:
        viewed_data = load_json(viewed_posts_file)
        viewed_accounts = extract_viewed_accounts(viewed_data)
    except FileNotFoundError:
        pass  # Continue processing if the file is not found

    try:
        liked_data = load_json(liked_posts_file)
        liked_accounts = extract_liked_accounts(liked_data)
    except FileNotFoundError:
        pass  # Continue processing if the file is not found

    accounts_viewed_not_liked = viewed_accounts - liked_accounts

    output_file = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts_viewed_not_liked:
            writer.writerow([account])

if __name__ == "__main__":
    main()