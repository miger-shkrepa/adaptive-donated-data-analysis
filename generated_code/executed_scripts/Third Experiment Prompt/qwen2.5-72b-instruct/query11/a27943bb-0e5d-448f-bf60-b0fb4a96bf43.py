import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_viewed_authors(posts_viewed_path):
    try:
        data = load_json(posts_viewed_path)
        viewed_authors = set()
        for entry in data.get("impressions_history_posts_seen", []):
            string_map_data = entry.get("string_map_data", {})
            author = string_map_data.get("Author", {}).get("value")
            if author:
                viewed_authors.add(author)
        return viewed_authors
    except Exception as e:
        print(f"Error processing {posts_viewed_path}: {e}")
        return set()

def get_liked_authors(liked_posts_path):
    try:
        data = load_json(liked_posts_path)
        liked_authors = set()
        for entry in data.get("likes_media_likes", []):
            for item in entry.get("string_list_data", []):
                liked_author = item.get("value")
                if liked_author:
                    liked_authors.add(liked_author)
        return liked_authors
    except Exception as e:
        print(f"Error processing {liked_posts_path}: {e}")
        return set()

def find_accounts_viewed_not_liked(root_dir):
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

    viewed_authors = get_viewed_authors(posts_viewed_path)
    liked_authors = get_liked_authors(liked_posts_path)

    accounts_viewed_not_liked = viewed_authors - liked_authors

    return accounts_viewed_not_liked

def save_to_csv(accounts, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV file {output_path}. Reason: {e}")

if __name__ == "__main__":
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        accounts_viewed_not_liked = find_accounts_viewed_not_liked(root_dir)
        save_to_csv(accounts_viewed_not_liked, 'query_responses/results.csv')
    except Exception as e:
        print(e)