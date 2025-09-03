import os
import json
import csv

root_dir = "root_dir"

def get_viewed_accounts(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            viewed_accounts = set()
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    viewed_accounts.add(author)
            return viewed_accounts
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def get_liked_accounts(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            liked_accounts = set()
            for entry in data.get("story_activities_story_likes", []):
                for sub_entry in entry.get("string_list_data", []):
                    liked_accounts.add(sub_entry.get("value", ""))
            return liked_accounts
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def find_accounts_viewed_not_liked(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")

        viewed_accounts = get_viewed_accounts(posts_viewed_path) if os.path.exists(posts_viewed_path) else set()
        liked_accounts = get_liked_accounts(story_likes_path) if os.path.exists(story_likes_path) else set()

        accounts_viewed_not_liked = viewed_accounts - liked_accounts

        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts_viewed_not_liked:
                writer.writerow([account])

    except Exception as e:
        print(f"An error occurred: {e}")

find_accounts_viewed_not_liked(root_dir)