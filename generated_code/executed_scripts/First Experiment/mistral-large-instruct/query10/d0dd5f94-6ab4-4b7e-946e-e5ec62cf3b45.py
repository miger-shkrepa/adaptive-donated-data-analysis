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
            post_views = []
            for entry in data.get('impressions_history_posts_seen', []):
                author = entry['string_map_data'].get('Author', {}).get('value', 'Unknown')
                time = entry['string_map_data'].get('Time', {}).get('timestamp', 0)
                post_views.append((author, time))
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
            video_views = []
            for entry in data.get('impressions_history_videos_watched', []):
                author = entry['string_map_data'].get('Author', {}).get('value', 'Unknown')
                time = entry['string_map_data'].get('Time', {}).get('timestamp', 0)
                video_views.append((author, time))
            return video_views
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Main function to process the directory
def process_directory(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    post_views_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    video_views_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')

    post_views = extract_post_views(post_views_file)
    video_views = extract_video_views(video_views_file)

    # Combine the data
    combined_data = {}
    for author, time in post_views:
        if author not in combined_data:
            combined_data[author] = {'Post Views': 0, 'Video Views': 0}
        combined_data[author]['Post Views'] += 1

    for author, time in video_views:
        if author not in combined_data:
            combined_data[author] = {'Post Views': 0, 'Video Views': 0}
        combined_data[author]['Video Views'] += 1

    # Write the results to a CSV file
    output_file = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for author, views in combined_data.items():
            writer.writerow({'Account': author, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

# Execute the main function
process_directory(root_dir)