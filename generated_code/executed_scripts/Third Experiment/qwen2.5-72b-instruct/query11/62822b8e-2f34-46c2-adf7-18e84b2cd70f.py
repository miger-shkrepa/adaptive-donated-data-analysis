import os
import json
import csv

root_dir = "root_dir"

def get_viewed_authors(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            authors = set()
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    authors.add(author)
            return authors
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def get_liked_authors(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            authors = set()
            for entry in data.get("media", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    authors.add(author)
            return authors
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def find_accounts_viewed_not_liked(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        liked_posts_path = os.path.join(root_dir, "media", "posts", "202308", "image.jpg")  # Placeholder for liked posts file

        if not os.path.exists(posts_viewed_path):
            return []

        viewed_authors = get_viewed_authors(posts_viewed_path)
        liked_authors = set()  # Assuming liked posts file is missing or not relevant

        if os.path.exists(liked_posts_path):
            liked_authors = get_liked_authors(liked_posts_path)

        accounts_viewed_not_liked = list(viewed_authors - liked_authors)
        return accounts_viewed_not_liked

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

accounts = find_accounts_viewed_not_liked(root_dir)

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account'])
    for account in accounts:
        writer.writerow([account])