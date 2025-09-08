import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract post views from posts_viewed.json
def extract_post_views(data):
    post_views = {}
    if 'impressions_history_posts_seen' in data:
        for entry in data['impressions_history_posts_seen']:
            author = entry['string_map_data']['Author']['value']
            if author not in post_views:
                post_views[author] = 0
            post_views[author] += 1
    return post_views

# Function to extract video views from reels.json and stories.json
def extract_video_views(data):
    video_views = {}
    if 'ig_reels_media' in data:
        for entry in data['ig_reels_media']:
            for media in entry['media']:
                if 'cross_post_source' in media and 'source_app' in media['cross_post_source']:
                    author = media['cross_post_source']['source_app']
                    if author not in video_views:
                        video_views[author] = 0
                    video_views[author] += 1
    if 'ig_stories' in data:
        for entry in data['ig_stories']:
            for media in entry['media_metadata']:
                if 'cross_post_source' in media and 'source_app' in media['cross_post_source']:
                    author = media['cross_post_source']['source_app']
                    if author not in video_views:
                        video_views[author] = 0
                    video_views[author] += 1
    return video_views

# Main function to process the data and generate the CSV
def main():
    # Initialize dictionaries to store post and video views
    post_views = {}
    video_views = {}

    # Path to posts_viewed.json
    posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    if os.path.exists(posts_viewed_path):
        posts_viewed_data = read_json_file(posts_viewed_path)
        post_views = extract_post_views(posts_viewed_data)

    # Path to reels.json
    reels_path = os.path.join(root_dir, 'your_instagram_activity', 'content', 'reels.json')
    if os.path.exists(reels_path):
        reels_data = read_json_file(reels_path)
        video_views = extract_video_views(reels_data)

    # Path to stories.json
    stories_path = os.path.join(root_dir, 'your_instagram_activity', 'content', 'stories.json')
    if os.path.exists(stories_path):
        stories_data = read_json_file(stories_path)
        video_views = extract_video_views(stories_data)

    # Combine post and video views into a single dictionary
    combined_views = {}
    for account, count in post_views.items():
        combined_views[account] = {'Post Views': count, 'Video Views': 0}
    for account, count in video_views.items():
        if account in combined_views:
            combined_views[account]['Video Views'] += count
        else:
            combined_views[account] = {'Post Views': 0, 'Video Views': count}

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in combined_views.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)