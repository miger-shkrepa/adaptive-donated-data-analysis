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
    if key in data:
        for entry in data[key]:
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                view_counts[author] = view_counts.get(author, 0) + 1
    return view_counts

def aggregate_views(posts_file, videos_file):
    try:
        posts_data = load_json_data(posts_file)
        videos_data = load_json_data(videos_file)
    except FileNotFoundError as e:
        print(e)
        return {}

    post_views = count_views(posts_data, "impressions_history_posts_seen")
    video_views = count_views(videos_data, "impressions_history_videos_watched")

    aggregated_views = {}
    for author, count in post_views.items():
        aggregated_views[author] = {'Post Views': count, 'Video Views': video_views.get(author, 0)}

    for author, count in video_views.items():
        if author not in aggregated_views:
            aggregated_views[author] = {'Post Views': post_views.get(author, 0), 'Video Views': count}

    return aggregated_views

def write_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in data.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

def main():
    posts_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        aggregated_views = aggregate_views(posts_file, videos_file)
        write_to_csv(aggregated_views, 'query_responses/results.csv')
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()