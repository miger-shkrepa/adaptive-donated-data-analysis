import os
import json
import csv

# Variable referring to the file input
root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def count_views(data, key):
    if not data:
        return {}
    views = {}
    for entry in data:
        author = entry.get('string_map_data', {}).get('Author', {}).get('value')
        if author:
            views[author] = views.get(author, 0) + 1
    return views

def main():
    # Define file paths
    posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_watched_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
    output_file = "query_responses/results.csv"

    # Initialize dictionaries to store counts
    post_views = {}
    video_views = {}

    # Load and process posts_viewed.json
    if os.path.exists(posts_viewed_file):
        try:
            posts_data = load_json_file(posts_viewed_file)
            post_views = count_views(posts_data.get('impressions_history_posts_seen', []), 'posts_viewed')
        except (FileNotFoundError, ValueError) as e:
            print(e)

    # Load and process videos_watched.json
    if os.path.exists(videos_watched_file):
        try:
            videos_data = load_json_file(videos_watched_file)
            video_views = count_views(videos_data.get('impressions_history_videos_watched', []), 'videos_watched')
        except (FileNotFoundError, ValueError) as e:
            print(e)

    # Combine the results into a list of dictionaries
    results = []
    all_authors = set(post_views.keys()).union(set(video_views.keys()))
    for author in all_authors:
        post_count = post_views.get(author, 0)
        video_count = video_views.get(author, 0)
        results.append({'Account': author, 'Post Views': post_count, 'Video Views': video_count})

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the results to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()