import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract topics of interest
def extract_topics_of_interest(root_dir):
    topics_of_interest = set()

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Define the paths to the relevant JSON files
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')

    # Function to read JSON file and extract topics
    def read_json_file(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        else:
            raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")

    # Extract topics from ads_viewed.json
    try:
        ads_viewed_data = read_json_file(ads_viewed_path)
        for ad in ads_viewed_data.get('impressions_history_ads_seen', []):
            topics_of_interest.add(ad.get('string_map_data', {}).get('Time', {}).get('timestamp', ''))
    except FileNotFoundError as e:
        print(e)

    # Extract topics from posts_viewed.json
    try:
        posts_viewed_data = read_json_file(posts_viewed_path)
        for post in posts_viewed_data.get('impressions_history_posts_seen', []):
            topics_of_interest.add(post.get('string_map_data', {}).get('Author', {}).get('value', ''))
    except FileNotFoundError as e:
        print(e)

    # Extract topics from videos_watched.json
    try:
        videos_watched_data = read_json_file(videos_watched_path)
        for video in videos_watched_data.get('impressions_history_videos_watched', []):
            topics_of_interest.add(video.get('string_map_data', {}).get('Time', {}).get('timestamp', ''))
    except FileNotFoundError as e:
        print(e)

    return list(topics_of_interest)

# Function to write the results to a CSV file
def write_to_csv(topics_of_interest, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Topics of Interest']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for topic in topics_of_interest:
            writer.writerow({'Topics of Interest': topic})

# Main function to execute the script
def main():
    try:
        topics_of_interest = extract_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest, output_csv)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()