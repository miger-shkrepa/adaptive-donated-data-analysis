import os
import json
import csv

root_dir = "root_dir"

def get_viewed_authors(posts_viewed_path):
    viewed_authors = set()
    try:
        with open(posts_viewed_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    viewed_authors.add(author)
    except FileNotFoundError:
        print("FileNotFoundError: The posts_viewed.json file does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON in posts_viewed.json.")
    return viewed_authors

def get_liked_authors(liked_posts_path):
    liked_authors = set()
    try:
        with open(liked_posts_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("likes_media_likes", []):
                for liked_post in entry.get("string_list_data", []):
                    liked_authors.add(liked_post.get("value"))
    except FileNotFoundError:
        print("FileNotFoundError: The liked_posts.json file does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON in liked_posts.json.")
    return liked_authors

def find_accounts_viewed_not_liked(root_dir):
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

    viewed_authors = get_viewed_authors(posts_viewed_path)
    liked_authors = get_liked_authors(liked_posts_path)

    accounts_viewed_not_liked = viewed_authors - liked_authors

    return accounts_viewed_not_liked

def write_to_csv(accounts, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        print(f"Error: Failed to write to CSV file. Reason: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    accounts_viewed_not_liked = find_accounts_viewed_not_liked(root_dir)
    output_path = 'query_responses/results.csv'
    write_to_csv(accounts_viewed_not_liked, output_path)