import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract topics of interest from the JSON files
def extract_topics_of_interest(root_dir):
    topics_of_interest = set()

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Define the paths to the relevant JSON files
    ads_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')

    # List of JSON files to process
    json_files = [ads_viewed_path, posts_viewed_path, videos_watched_path]

    # Process each JSON file
    for file_path in json_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for item in data.get('impressions_history_ads_seen', []):
                        topics_of_interest.add(item.get('string_map_data', {}).get('Author', {}).get('value', ''))
                    for item in data.get('impressions_history_posts_seen', []):
                        topics_of_interest.add(item.get('string_map_data', {}).get('Author', {}).get('value', ''))
                    for item in data.get('impressions_history_videos_watched', []):
                        topics_of_interest.add(item.get('string_map_data', {}).get('Author', {}).get('value', ''))
            except json.JSONDecodeError:
                raise ValueError("Error: Failed to decode JSON file.")

    return topics_of_interest

# Function to write the results to a CSV file
def write_to_csv(topics_of_interest, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
        for topic in topics_of_interest:
            writer.writerow([topic])

# Main function to execute the script
def main():
    try:
        topics_of_interest = extract_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest, output_csv)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()