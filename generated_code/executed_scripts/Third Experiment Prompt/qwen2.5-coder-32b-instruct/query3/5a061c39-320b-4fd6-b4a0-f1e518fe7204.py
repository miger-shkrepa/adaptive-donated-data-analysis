import os
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output file path
output_file_path = "query_responses/results.csv"

# Function to parse the timestamp and return the date or week
def parse_timestamp(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date.strftime('%Y-%m-%d'), date.strftime('Week %Y-%W')

# Function to read and parse JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to process posts viewed data
def process_posts_viewed_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}

    for entry in posts_viewed_data.get('impressions_history_posts_seen', []):
        string_map_data = entry.get('string_map_data', {})
        timestamp = string_map_data.get('Time', {}).get('timestamp', None)
        if timestamp:
            date_str, week_str = parse_timestamp(timestamp)
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
            weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1

    return daily_counts, weekly_counts

# Main function to generate the CSV file
def generate_csv(root_dir, output_file_path):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize the data structures
        daily_counts = {}
        weekly_counts = {}

        # Define the path to the posts_viewed.json file
        posts_viewed_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

        # Check if the posts_viewed.json file exists
        if os.path.exists(posts_viewed_file_path):
            # Read and parse the posts_viewed.json file
            posts_viewed_data = read_json_file(posts_viewed_file_path)

            # Process the posts viewed data
            daily_counts, weekly_counts = process_posts_viewed_data(posts_viewed_data)

        # Prepare the CSV data
        csv_data = []
        for date, count in daily_counts.items():
            csv_data.append([date, count, 'Daily'])
        for week, count in weekly_counts.items():
            csv_data.append([week, count, 'Weekly'])

        # Sort the CSV data by date/week
        csv_data.sort(key=lambda x: (x[2], x[0]))

        # Write the CSV file
        with open(output_file_path, 'w', encoding='utf-8') as csv_file:
            csv_file.write("Date/Week,Posts Viewed,Type\n")
            for row in csv_data:
                csv_file.write(f"{row[0]},{row[1]},{row[2]}\n")

    except Exception as e:
        # Handle any exceptions and write only the column headers
        with open(output_file_path, 'w', encoding='utf-8') as csv_file:
            csv_file.write("Date/Week,Posts Viewed,Type\n")

# Generate the CSV file
generate_csv(root_dir, output_file_path)