import os
import json
import csv

root_dir = "root_dir"

def get_viewed_accounts(posts_viewed_path):
    viewed_accounts = set()
    try:
        with open(posts_viewed_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    viewed_accounts.add(author)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: posts_viewed.json is not a valid JSON file.")
    return viewed_accounts

def get_liked_accounts(liked_comments_path):
    liked_accounts = set()
    try:
        with open(liked_comments_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data.get("liked_comments", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    liked_accounts.add(author)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The liked_comments.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: liked_comments.json is not a valid JSON file.")
    return liked_accounts

def find_accounts_viewed_not_liked(root_dir):
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    liked_comments_path = os.path.join(root_dir, "likes", "liked_comments.json")

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    if not os.path.exists(posts_viewed_path) or not os.path.exists(liked_comments_path):
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
        return

    viewed_accounts = get_viewed_accounts(posts_viewed_path)
    liked_accounts = get_liked_accounts(liked_comments_path)

    accounts_viewed_not_liked = viewed_accounts - liked_accounts

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts_viewed_not_liked:
            writer.writerow([account])

try:
    find_accounts_viewed_not_liked(root_dir)
except Exception as e:
    print(e)