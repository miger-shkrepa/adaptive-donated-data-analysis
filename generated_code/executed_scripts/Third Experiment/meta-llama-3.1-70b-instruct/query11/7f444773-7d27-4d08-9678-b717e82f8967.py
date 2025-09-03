import os
import json
import csv

root_dir = "root_dir"

def get_viewed_posts(root_dir):
    try:
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if not os.path.exists(posts_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
        with open(posts_viewed_path, 'r') as file:
            posts_viewed_data = json.load(file)
            viewed_authors = [post["string_map_data"]["Author"]["value"] for post in posts_viewed_data["impressions_history_posts_seen"]]
            return viewed_authors
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_liked_posts(root_dir):
    try:
        liked_posts_path = os.path.join(root_dir, "connections", "subscriptions", "reels.json")
        if not os.path.exists(liked_posts_path):
            return []
        with open(liked_posts_path, 'r') as file:
            liked_posts_data = json.load(file)
            liked_authors = [post["string_map_data"]["Benutzername"]["value"] for post in liked_posts_data["subscriptions_reels"]]
            return liked_authors
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_accounts_not_liked(root_dir):
    try:
        viewed_authors = get_viewed_posts(root_dir)
        liked_authors = get_liked_posts(root_dir)
        not_liked_authors = [author for author in viewed_authors if author not in liked_authors]
        return not_liked_authors
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts, csv_path):
    try:
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        accounts_not_liked = get_accounts_not_liked(root_dir)
        csv_path = 'query_responses/results.csv'
        save_to_csv(accounts_not_liked, csv_path)
    except Exception as e:
        if "FileNotFoundError" in str(e):
            csv_path = 'query_responses/results.csv'
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Account"])
        else:
            raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()