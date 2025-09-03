import json
import os
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def count_views(data, key):
    view_counts = {}
    if data and key in data:
        for entry in data[key]:
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                view_counts[author] = view_counts.get(author, 0) + 1
    return view_counts

def process_data(root_dir):
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

    posts_viewed_data = {}
    videos_watched_data = {}

    try:
        if os.path.exists(posts_viewed_path):
            posts_viewed_data = load_json_data(posts_viewed_path)
            posts_viewed_data = count_views(posts_viewed_data, "impressions_history_posts_seen")
    except Exception as e:
        print(f"Error processing posts_viewed.json: {e}")

    try:
        if os.path.exists(videos_watched_path):
            videos_watched_data = load_json_data(videos_watched_path)
            videos_watched_data = count_views(videos_watched_data, "impressions_history_videos_watched")
    except Exception as e:
        print(f"Error processing videos_watched.json: {e}")

    result = {}
    for author, count in posts_viewed_data.items():
        result[author] = [count, videos_watched_data.get(author, 0)]

    for author, count in videos_watched_data.items():
        if author not in result:
            result[author] = [posts_viewed_data.get(author, 0), count]
        else:
            result[author][1] = count

    return result

def save_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in data.items():
            writer.writerow({'Account': account, 'Post Views': views[0], 'Video Views': views[1]})

if __name__ == "__main__":
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        result_data = process_data(root_dir)
        save_to_csv(result_data, 'query_responses/results.csv')
    except Exception as e:
        print(f"Error: {e}")
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()