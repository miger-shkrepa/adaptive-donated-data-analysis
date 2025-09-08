import os
import json
import csv

root_dir = "root_dir"

def get_accounts(root_dir):
    accounts_viewed = set()
    accounts_liked = set()

    try:
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(posts_viewed_path):
            with open(posts_viewed_path, "r") as f:
                data = json.load(f)
                for post in data["impressions_history_posts_seen"]:
                    accounts_viewed.add(post["string_map_data"]["Author"]["value"])

        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, "r") as f:
                data = json.load(f)
                for post in data["likes_media_likes"]:
                    accounts_liked.add(post["string_list_data"][0]["value"])

        accounts_not_liked = accounts_viewed - accounts_liked
        return list(accounts_not_liked)

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Invalid JSON format in one of the files.")
    except KeyError:
        raise ValueError("Error: Missing key in one of the files.")

def write_to_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

accounts = get_accounts(root_dir)
if accounts:
    write_to_csv(accounts)
else:
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])