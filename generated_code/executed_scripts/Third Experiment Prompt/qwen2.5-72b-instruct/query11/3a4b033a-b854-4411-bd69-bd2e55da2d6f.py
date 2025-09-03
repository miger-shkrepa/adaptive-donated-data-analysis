import os
import json
import csv

root_dir = "root_dir"

def get_viewed_authors(root_dir):
    viewed_authors = set()
    ads_and_topics_path = os.path.join(root_dir, "ads_information", "ads_and_topics")
    
    if not os.path.exists(ads_and_topics_path):
        return viewed_authors

    for filename in ["ads_viewed.json", "posts_viewed.json", "videos_watched.json"]:
        file_path = os.path.join(ads_and_topics_path, filename)
        if not os.path.exists(file_path):
            continue

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                for entry in data.get("impressions_history_ads_seen", []) + data.get("impressions_history_posts_seen", []) + data.get("impressions_history_videos_watched", []):
                    author = entry.get("string_map_data", {}).get("Author", {}).get("value")
                    if author:
                        viewed_authors.add(author)
            except json.JSONDecodeError:
                raise ValueError("Error: Failed to decode JSON in file: " + file_path)
    
    return viewed_authors

def get_liked_authors(root_dir):
    liked_authors = set()
    likes_path = os.path.join(root_dir, "your_instagram_activity", "likes")
    
    if not os.path.exists(likes_path):
        return liked_authors

    liked_posts_file = os.path.join(likes_path, "liked_posts.json")
    if not os.path.exists(liked_posts_file):
        return liked_authors

    with open(liked_posts_file, 'r') as file:
        try:
            data = json.load(file)
            for entry in data.get("likes_media_likes", []):
                for liked_post in entry.get("string_list_data", []):
                    author = liked_post.get("value")
                    if author:
                        liked_authors.add(author)
        except json.JSONDecodeError:
            raise ValueError("Error: Failed to decode JSON in file: " + liked_posts_file)
    
    return liked_authors

def find_accounts_viewed_not_liked(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    viewed_authors = get_viewed_authors(root_dir)
    liked_authors = get_liked_authors(root_dir)

    accounts_viewed_not_liked = viewed_authors - liked_authors

    return accounts_viewed_not_liked

def save_to_csv(accounts, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

try:
    accounts_viewed_not_liked = find_accounts_viewed_not_liked(root_dir)
    save_to_csv(accounts_viewed_not_liked, 'query_responses/results.csv')
except Exception as e:
    print(e)
    save_to_csv([], 'query_responses/results.csv')