import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def process_ads_and_topics(data):
    post_views = 0
    video_views = 0
    accounts = set()

    if "impressions_history_posts_seen" in data:
        for item in data["impressions_history_posts_seen"]:
            if "string_map_data" in item:
                string_map_data = item["string_map_data"]
                if "Author" in string_map_data and "Time" in string_map_data:
                    accounts.add(string_map_data["Author"]["value"])
                    post_views += 1

    return accounts, post_views, video_views

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        ads_and_topics_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if not os.path.exists(ads_and_topics_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Account", "Post Views", "Video Views"])
            return

        ads_and_topics_data = load_json(ads_and_topics_path)
        accounts, post_views, video_views = process_ads_and_topics(ads_and_topics_data)

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account", "Post Views", "Video Views"])
            for account in accounts:
                writer.writerow([account, post_views, video_views])

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()