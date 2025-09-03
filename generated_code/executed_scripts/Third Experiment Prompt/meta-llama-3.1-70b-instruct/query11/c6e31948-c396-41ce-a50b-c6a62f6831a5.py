import os
import json
import csv

root_dir = "root_dir"

def get_accounts(root_dir):
    accounts_viewed = set()
    accounts_liked = set()

    try:
        # Get accounts viewed
        posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(posts_viewed_file):
            with open(posts_viewed_file, "r") as f:
                data = json.load(f)
                for post in data["impressions_history_posts_seen"]:
                    accounts_viewed.add(post["string_map_data"]["Author"]["value"])
        else:
            raise FileNotFoundError("Error: The file 'posts_viewed.json' does not exist.")

        # Get accounts liked
        liked_posts_file = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(liked_posts_file):
            with open(liked_posts_file, "r") as f:
                data = json.load(f)
                for post in data["likes_media_likes"]:
                    accounts_liked.add(post["string_list_data"][0]["value"])
        else:
            raise FileNotFoundError("Error: The file 'liked_posts.json' does not exist.")

        # Get accounts viewed but not liked
        accounts_viewed_but_not_liked = accounts_viewed - accounts_liked

        return accounts_viewed_but_not_liked

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")

def write_to_csv(accounts):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])  # header
        for account in accounts:
            writer.writerow([account])

def main():
    try:
        accounts = get_accounts(root_dir)
        write_to_csv(accounts)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])  # header

if __name__ == "__main__":
    main()