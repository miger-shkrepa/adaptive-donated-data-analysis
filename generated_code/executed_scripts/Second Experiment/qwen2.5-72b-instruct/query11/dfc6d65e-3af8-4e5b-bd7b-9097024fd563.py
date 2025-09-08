import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

def get_viewed_authors():
    try:
        file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        data = load_json(file_path)
        viewed_authors = set()
        for entry in data.get("impressions_history_posts_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                viewed_authors.add(author)
        return viewed_authors
    except Exception as e:
        print(f"Error: {e}")
        return set()

def get_liked_authors():
    try:
        file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_you're_not_interested_in.json")
        data = load_json(file_path)
        liked_authors = set()
        for entry in data.get("impressions_history_posts_not_interested", []):
            for item in entry.get("string_list_data", []):
                href = item.get("href")
                if href:
                    liked_authors.add(href)
        return liked_authors
    except Exception as e:
        print(f"Error: {e}")
        return set()

def find_accounts_viewed_not_liked():
    viewed_authors = get_viewed_authors()
    liked_authors = get_liked_authors()
    accounts_viewed_not_liked = viewed_authors - liked_authors
    return accounts_viewed_not_liked

def save_to_csv(accounts):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

try:
    accounts_viewed_not_liked = find_accounts_viewed_not_liked()
    save_to_csv(accounts_viewed_not_liked)
except Exception as e:
    print(f"Error: {e}")
    save_to_csv([])