import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to parse JSON files and extract relevant data
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
        date = datetime.fromtimestamp(timestamp)
        date_str = date.strftime('%Y-%m-%d')
        week_str = f"Week {date.strftime('%Y-%W')}"

        if date_str not in posts_viewed:
            posts_viewed[date_str] = {'Daily': 0, 'Weekly': 0}
        if week_str not in posts_viewed:
            posts_viewed[week_str] = {'Daily': 0, 'Weekly': 0}

        posts_viewed[date_str]['Daily'] += 1
        posts_viewed[week_str]['Weekly'] += 1

    return posts_viewed

# Main function to process the directory and generate the CSV file
def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

        # Path to the posts_viewed.json file
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

        # Parse the posts_viewed.json file
        posts_viewed_data = parse_json_file(posts_viewed_path)

        # Process the posts viewed data
        posts_viewed = process_posts_viewed(posts_viewed_data)

        # Prepare the CSV data
        csv_data = [['Date/Week', 'Posts Viewed', 'Type']]
        for date_week, counts in posts_viewed.items():
            csv_data.append([date_week, counts['Daily'], 'Daily'])
            csv_data.append([date_week, counts['Weekly'], 'Weekly'])

        # Write the CSV data to a file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()