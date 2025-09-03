import os
import json
import csv

root_dir = "root_dir"

def get_account_info(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize sets to store viewed and liked accounts
        viewed_accounts = set()
        liked_accounts = set()

        # Iterate through ads_and_topics directory
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if os.path.exists(ads_and_topics_dir):
            # Get viewed accounts from posts_viewed.json
            posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
            if os.path.exists(posts_viewed_file):
                with open(posts_viewed_file, "r") as file:
                    data = json.load(file)
                    for post in data["impressions_history_posts_seen"]:
                        viewed_accounts.add(post["string_map_data"]["Author"]["value"])

            # Get liked accounts from in-app_message.json (assuming likes are stored in in-app messages)
            in_app_message_file = os.path.join(ads_and_topics_dir, "in-app_message.json")
            if os.path.exists(in_app_message_file):
                with open(in_app_message_file, "r") as file:
                    data = json.load(file)
                    for message in data["impressions_history_app_message"]:
                        if message["string_map_data"]["Click type"]["value"] == "Like":
                            liked_accounts.add(message["string_map_data"]["In-app message name"]["value"])

        # Find accounts that have been viewed but not liked
        not_liked_accounts = viewed_accounts - liked_accounts

        return not_liked_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(accounts):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        accounts = get_account_info(root_dir)
        write_to_csv(accounts)

    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
        raise FileNotFoundError("FileNotFoundError: " + str(e))

    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()