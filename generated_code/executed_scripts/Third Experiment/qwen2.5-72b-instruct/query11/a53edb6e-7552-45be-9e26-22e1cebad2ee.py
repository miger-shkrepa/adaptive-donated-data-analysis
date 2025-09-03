import os
import json
import csv

root_dir = "root_dir"

def get_viewed_accounts(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            viewed_accounts = set()
            for post in data.get("impressions_history_posts_seen", []):
                author = post.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    viewed_accounts.add(author)
            return viewed_accounts
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def get_liked_accounts(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            liked_accounts = set()
            for like in data.get("likes_media_likes", []):
                for entry in like.get("string_list_data", []):
                    account = entry.get("value")
                    if account:
                        liked_accounts.add(account)
            return liked_accounts
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def find_accounts_viewed_not_liked(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        viewed_accounts_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        liked_accounts_file = os.path.join(root_dir, "likes", "liked_posts.json")

        viewed_accounts = set()
        liked_accounts = set()

        if os.path.exists(viewed_accounts_file):
            viewed_accounts = get_viewed_accounts(viewed_accounts_file)
        else:
            print("Warning: posts_viewed.json does not exist. Assuming no posts viewed.")

        if os.path.exists(liked_accounts_file):
            liked_accounts = get_liked_accounts(liked_accounts_file)
        else:
            print("Warning: liked_posts.json does not exist. Assuming no posts liked.")

        accounts_viewed_not_liked = viewed_accounts - liked_accounts

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts_viewed_not_liked:
                writer.writerow([account])

    except Exception as e:
        print(f"An error occurred: {e}")

find_accounts_viewed_not_liked(root_dir)