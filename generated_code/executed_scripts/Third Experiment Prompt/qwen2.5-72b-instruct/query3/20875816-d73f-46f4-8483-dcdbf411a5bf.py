import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to load JSON data from a file
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

# Function to process posts_viewed.json and extract timestamps
def process_posts_viewed(posts_viewed_data):
    timestamps = []
    for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
        string_map_data = entry.get("string_map_data", {})
        time_data = string_map_data.get("Time", {})
        timestamp = time_data.get("timestamp")
        if timestamp:
            timestamps.append(datetime.fromtimestamp(timestamp / 1000))
    return timestamps

# Function to aggregate daily and weekly counts
def aggregate_counts(timestamps):
    daily_counts = {}
    weekly_counts = {}

    for timestamp in timestamps:
        date_str = timestamp.strftime('%Y-%m-%d')
        week_str = f"Week {timestamp.strftime('%Y-%W')}"

        if date_str in daily_counts:
            daily_counts[date_str] += 1
        else:
            daily_counts[date_str] = 1

        if week_str in weekly_counts:
            weekly_counts[week_str] += 1
        else:
            weekly_counts[week_str] = 1

    return daily_counts, weekly_counts

# Function to write results to CSV
def write_to_csv(daily_counts, weekly_counts):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to process the data
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(posts_viewed_path):
            write_to_csv({}, {})
            return

        posts_viewed_data = load_json(posts_viewed_path)
        timestamps = process_posts_viewed(posts_viewed_data)
        daily_counts, weekly_counts = aggregate_counts(timestamps)
        write_to_csv(daily_counts, weekly_counts)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()