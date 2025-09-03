import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract post views
def extract_post_views(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            post_views = {}
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry["string_map_data"]["Author"]["value"]
                time = entry["string_map_data"]["Time"]["timestamp"]
                if author in post_views:
                    post_views[author] += 1
                else:
                    post_views[author] = 1
            return post_views
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to extract video views
def extract_video_views(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            video_views = {}
            for entry in data.get("impressions_history_videos_watched", []):
                author = entry["string_map_data"]["Author"]["value"]
                time = entry["string_map_data"]["Time"]["timestamp"]
                if author in video_views:
                    video_views[author] += 1
                else:
                    video_views[author] = 1
            return video_views
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Main function to process the directory
def process_directory(root_dir):
    post_views_file = os.path.join(root_dir, "posts_viewed.json")
    video_views_file = os.path.join(root_dir, "videos_watched.json")

    post_views = {}
    video_views = {}

    if os.path.exists(post_views_file):
        post_views = extract_post_views(post_views_file)

    if os.path.exists(video_views_file):
        video_views = extract_video_views(video_views_file)

    # Combine the results
    accounts = set(post_views.keys()).union(set(video_views.keys()))
    results = []

    for account in accounts:
        post_count = post_views.get(account, 0)
        video_count = video_views.get(account, 0)
        results.append([account, post_count, video_count])

    # Write the results to a CSV file
    output_file = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])
        writer.writerows(results)

# Run the main function
try:
    process_directory(root_dir)
except Exception as e:
    print(e)