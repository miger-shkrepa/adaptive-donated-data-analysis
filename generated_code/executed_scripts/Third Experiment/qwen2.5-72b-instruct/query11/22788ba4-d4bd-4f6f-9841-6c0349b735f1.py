import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")

def find_viewed_not_liked_accounts(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        viewed_posts_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

        viewed_posts_data = load_json_data(viewed_posts_path) if os.path.exists(viewed_posts_path) else {}
        liked_posts_data = load_json_data(liked_posts_path) if os.path.exists(liked_posts_path) else {}

        viewed_authors = set()
        liked_authors = set()

        for entry in viewed_posts_data.get("impressions_history_posts_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                viewed_authors.add(author)

        for entry in liked_posts_data.get("likes_media_likes", []):
            for data in entry.get("string_list_data", []):
                author = data.get("value")
                if author:
                    liked_authors.add(author)

        not_liked_accounts = viewed_authors - liked_authors

        return not_liked_accounts

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(accounts, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file. {str(e)}")

try:
    not_liked_accounts = find_viewed_not_liked_accounts(root_dir)
    write_to_csv(not_liked_accounts, 'query_responses/results.csv')
except Exception as e:
    print(str(e))
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])