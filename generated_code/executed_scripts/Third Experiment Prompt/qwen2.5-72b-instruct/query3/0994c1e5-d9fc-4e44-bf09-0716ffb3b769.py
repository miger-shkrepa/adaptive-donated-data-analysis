import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to load JSON data from a file
def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

# Function to process posts viewed data
def process_posts_viewed(posts_viewed_data):
    posts_viewed = []
    for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
        string_map_data = entry.get("string_map_data", {})
        timestamp = string_map_data.get("Time", {}).get("timestamp")
        if timestamp:
            date = datetime.fromtimestamp(timestamp)
            posts_viewed.append(date)
    return posts_viewed

# Function to aggregate daily and weekly counts
def aggregate_counts(posts_viewed):
    daily_counts = {}
    weekly_counts = {}

    for date in posts_viewed:
        date_str = date.strftime('%Y-%m-%d')
        week_str = f"Week {date.strftime('%Y-%W')}"

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

        for date_str, count in daily_counts.items():
            writer.writerow({'Date/Week': date_str, 'Posts Viewed': count, 'Type': 'Daily'})

        for week_str, count in weekly_counts.items():
            writer.writerow({'Date/Week': week_str, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to execute the query
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(posts_viewed_path):
            write_to_csv({}, {})
            return

        posts_viewed_data = load_json_data(posts_viewed_path)
        posts_viewed = process_posts_viewed(posts_viewed_data)
        daily_counts, weekly_counts = aggregate_counts(posts_viewed)
        write_to_csv(daily_counts, weekly_counts)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()