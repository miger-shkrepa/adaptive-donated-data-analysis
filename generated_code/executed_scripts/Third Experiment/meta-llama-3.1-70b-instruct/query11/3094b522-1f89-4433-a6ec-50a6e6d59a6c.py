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
        liked_posts_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_you're_not_interested_in.json")
        if not os.path.exists(liked_posts_path):
            raise FileNotFoundError("FileNotFoundError: The posts_you're_not_interested_in.json file does not exist.")
        with open(liked_posts_path, 'r') as file:
            liked_posts_data = json.load(file)
            liked_authors = [post["string_list_data"][0]["value"] for post in liked_posts_data["impressions_history_posts_not_interested"]]
            return liked_authors
    except Exception as e:
        raise ValueError("Error: " + str(e))

def get_accounts(root_dir):
    try:
        viewed_authors = get_viewed_posts(root_dir)
        liked_authors = get_liked_posts(root_dir)
        accounts = [author for author in viewed_authors if author not in liked_authors]
        return accounts
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
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
        accounts = get_accounts(root_dir)
        save_to_csv(accounts)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()