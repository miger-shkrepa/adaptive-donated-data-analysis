import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse the JSON file and extract the required data
def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to process the posts viewed data
def process_posts_viewed(data):
    posts_viewed = {}
    for entry in data.get('impressions_history_posts_seen', []):
        timestamp = entry['string_map_data']['Time']['timestamp']
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        week = datetime.fromtimestamp(timestamp).strftime('Week %Y-%W')
        posts_viewed[date] = posts_viewed.get(date, 0) + 1
        posts_viewed[week] = posts_viewed.get(week, 0) + 1
    return posts_viewed

# Function to write the results to a CSV file
def write_to_csv(data):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in data.items():
            if 'Week' in key:
                writer.writerow({'Date/Week': key, 'Posts Viewed': value, 'Type': 'Weekly'})
            else:
                writer.writerow({'Date/Week': key, 'Posts Viewed': value, 'Type': 'Daily'})

# Main function to process the directory and generate the CSV file
def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

        # Path to the posts_viewed.json file
        posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

        # Parse the posts_viewed.json file
        posts_viewed_data = parse_json_file(posts_viewed_file)

        # Process the posts viewed data
        posts_viewed_counts = process_posts_viewed(posts_viewed_data)

        # Write the results to a CSV file
        write_to_csv(posts_viewed_counts)

    except Exception as e:
        print(e)
        # If an error occurs, create a CSV file with only the column headers
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()