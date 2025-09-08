import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_viewed_accounts():
    try:
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        posts_viewed_data = load_json_data(posts_viewed_path)
        viewed_accounts = set()
        for entry in posts_viewed_data["impressions_history_posts_seen"]:
            for data in entry["string_map_data"]:
                if "Author" in data:
                    viewed_accounts.add(data["Author"]["value"])
        return viewed_accounts
    except FileNotFoundError:
        return set()

def get_liked_accounts():
    try:
        story_likes_path = os.path.join(root_dir, "connections", "story_activities_story_likes.json")
        story_likes_data = load_json_data(story_likes_path)
        liked_accounts = set()
        for entry in story_likes_data["story_activities_story_likes"]:
            for data in entry["string_list_data"]:
                liked_accounts.add(data["value"])
        return liked_accounts
    except FileNotFoundError:
        return set()

def find_accounts_viewed_not_liked():
    viewed_accounts = get_viewed_accounts()
    liked_accounts = get_liked_accounts()
    accounts_viewed_not_liked = viewed_accounts - liked_accounts
    return accounts_viewed_not_liked

def write_to_csv(accounts):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    accounts_viewed_not_liked = find_accounts_viewed_not_liked()
    write_to_csv(accounts_viewed_not_liked)
except Exception as e:
    print(e)