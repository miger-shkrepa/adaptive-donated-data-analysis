import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract post and video views
def extract_views(root_dir):
    post_views = []
    video_views = []

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Define the paths for the JSON files
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

    # Extract post views
    try:
        with open(posts_viewed_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value", "")
                time = entry.get("string_map_data", {}).get("Time", {}).get("timestamp", 0)
                post_views.append((author, time))
    except FileNotFoundError:
        raise FileNotFoundError("Error: The posts_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The posts_viewed.json file is not a valid JSON.")

    # Extract video views
    try:
        with open(videos_watched_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("impressions_history_videos_watched", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value", "")
                time = entry.get("string_map_data", {}).get("Time", {}).get("timestamp", 0)
                video_views.append((author, time))
    except FileNotFoundError:
        raise FileNotFoundError("Error: The videos_watched.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The videos_watched.json file is not a valid JSON.")

    return post_views, video_views

# Function to write the results to a CSV file
def write_to_csv(post_views, video_views):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Combine post and video views into a single dictionary
        views_dict = {}
        for author, time in post_views:
            if author not in views_dict:
                views_dict[author] = {'Post Views': 0, 'Video Views': 0}
            views_dict[author]['Post Views'] += 1

        for author, time in video_views:
            if author not in views_dict:
                views_dict[author] = {'Post Views': 0, 'Video Views': 0}
            views_dict[author]['Video Views'] += 1

        # Write the combined views to the CSV file
        for author, views in views_dict.items():
            writer.writerow({'Account': author, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

# Main function to execute the script
def main():
    post_views, video_views = extract_views(root_dir)
    write_to_csv(post_views, video_views)

if __name__ == "__main__":
    main()