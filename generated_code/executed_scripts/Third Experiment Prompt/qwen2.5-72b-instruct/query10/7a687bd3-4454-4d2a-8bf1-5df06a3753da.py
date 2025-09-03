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

def process_ads_and_topics(data_dir):
    post_views = 0
    video_views = 0
    accounts = set()

    try:
        ads_and_topics_dir = os.path.join(data_dir, 'ads_information', 'ads_and_topics')
        if not os.path.exists(ads_and_topics_dir):
            return post_views, video_views, accounts

        for file_name in ['ads_viewed.json', 'posts_viewed.json', 'videos_watched.json']:
            file_path = os.path.join(ads_and_topics_dir, file_name)
            if os.path.exists(file_path):
                data = load_json(file_path)
                if file_name == 'posts_viewed.json':
                    for entry in data.get('impressions_history_posts_seen', []):
                        for string_map in entry.get('string_map_data', []):
                            accounts.add(string_map.get('Author', {}).get('value', 'Unknown'))
                        post_views += len(entry.get('string_map_data', []))
                elif file_name == 'videos_watched.json':
                    for entry in data.get('impressions_history_videos_watched', []):
                        for string_map in entry.get('string_map_data', []):
                            accounts.add(string_map.get('Author', {}).get('value', 'Unknown'))
                        video_views += len(entry.get('string_map_data', []))
    except Exception as e:
        print(f"Error processing ads_and_topics: {e}")

    return post_views, video_views, accounts

def write_csv(post_views, video_views, accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if not accounts:
                return
            for account in accounts:
                writer.writerow({'Account': account, 'Post Views': post_views, 'Video Views': video_views})
    except Exception as e:
        raise ValueError(f"Error: Failed to write CSV file. Reason: {e}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        post_views, video_views, accounts = process_ads_and_topics(root_dir)
        write_csv(post_views, video_views, accounts)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()