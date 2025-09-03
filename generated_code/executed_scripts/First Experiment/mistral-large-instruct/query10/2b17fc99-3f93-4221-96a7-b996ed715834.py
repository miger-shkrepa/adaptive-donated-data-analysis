import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract data from JSON files
def extract_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to process the data and generate the CSV
def process_data(root_dir):
    posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')

    posts_data = extract_data(posts_viewed_path)
    videos_data = extract_data(videos_watched_path)

    results = []

    # Process posts viewed data
    for post in posts_data.get('impressions_history_posts_seen', []):
        author = post['string_map_data'].get('Author', {}).get('value', 'Unknown')
        time = post['string_map_data'].get('Time', {}).get('timestamp', 0)
        results.append((author, time, 0))

    # Process videos watched data
    for video in videos_data.get('impressions_history_videos_watched', []):
        author = video['string_map_data'].get('Author', {}).get('value', 'Unknown')
        time = video['string_map_data'].get('Time', {}).get('timestamp', 0)
        results.append((author, 0, time))

    # Aggregate the results
    aggregated_results = {}
    for author, post_views, video_views in results:
        if author not in aggregated_results:
            aggregated_results[author] = {'Post Views': 0, 'Video Views': 0}
        aggregated_results[author]['Post Views'] += post_views
        aggregated_results[author]['Video Views'] += video_views

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for author, data in aggregated_results.items():
            writer.writerow({'Account': author, 'Post Views': data['Post Views'], 'Video Views': data['Video Views']})

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    process_data(root_dir)

if __name__ == "__main__":
    main()