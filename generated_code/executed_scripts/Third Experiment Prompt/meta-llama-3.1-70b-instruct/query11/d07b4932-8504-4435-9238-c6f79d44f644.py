import os
import json
import csv

root_dir = "root_dir"

def get_accounts(root_dir):
    accounts_viewed = set()
    accounts_liked = set()

    try:
        ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if os.path.exists(ads_info_dir):
            posts_viewed_file = os.path.join(ads_info_dir, "posts_viewed.json")
            if os.path.exists(posts_viewed_file):
                with open(posts_viewed_file, "r") as f:
                    data = json.load(f)
                    for post in data["impressions_history_posts_seen"]:
                        accounts_viewed.add(post["string_map_data"]["Author"]["value"])

        connections_dir = os.path.join(root_dir, "connections", "followers_and_following")
        if os.path.exists(connections_dir):
            liked_posts_file = os.path.join(connections_dir, "liked_posts.json")
            if os.path.exists(liked_posts_file):
                with open(liked_posts_file, "r") as f:
                    data = json.load(f)
                    for post in data["likes_media_likes"]:
                        accounts_liked.add(post["string_list_data"][0]["value"])

        accounts_not_liked = accounts_viewed - accounts_liked
        return list(accounts_not_liked)

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory or required files do not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Invalid JSON format in one of the files.")
    except Exception as e:
        raise Exception("Error: An unexpected error occurred - " + str(e))

def write_to_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

accounts = get_accounts(root_dir)
write_to_csv(accounts)