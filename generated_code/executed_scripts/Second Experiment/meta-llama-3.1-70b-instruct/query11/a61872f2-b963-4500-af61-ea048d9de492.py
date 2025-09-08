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

        # Iterate over ads_and_topics directory
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if os.path.exists(ads_and_topics_dir):
            for filename in os.listdir(ads_and_topics_dir):
                if filename == "posts_viewed.json":
                    # Load posts_viewed.json file
                    with open(os.path.join(ads_and_topics_dir, filename), "r") as file:
                        data = json.load(file)
                        for post in data["impressions_history_posts_seen"]:
                            viewed_accounts.add(post["string_map_data"]["Author"]["value"])
                elif filename == "in-app_message.json":
                    # Load in-app_message.json file
                    with open(os.path.join(ads_and_topics_dir, filename), "r") as file:
                        data = json.load(file)
                        for message in data["impressions_history_app_message"]:
                            if message["string_map_data"]["Click type"]["value"] == "Like":
                                liked_accounts.add(message["string_map_data"]["In-app message name"]["value"])

        # Find accounts that have been viewed but not liked
        not_liked_accounts = viewed_accounts - liked_accounts

        # Write results to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in not_liked_accounts:
                writer.writerow([account])

    except FileNotFoundError as e:
        # If a required file does not exist, write a CSV file with only the column headers
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
        raise FileNotFoundError("FileNotFoundError: " + str(e))

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON file - " + str(e))

    except Exception as e:
        raise ValueError("Error: An unexpected error occurred - " + str(e))

get_account_info(root_dir)