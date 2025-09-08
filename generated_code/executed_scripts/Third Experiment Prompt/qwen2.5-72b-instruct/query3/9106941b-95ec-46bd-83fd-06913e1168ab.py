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
def process_posts_viewed_data(posts_viewed_data):
    posts_viewed = []
    for entry in posts_viewed_data:
        string_map_data = entry.get("string_map_data", {})
        time_str = string_map_data.get("Time", {}).get("timestamp")
        if time_str:
            timestamp = int(time_str)
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
        daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1
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
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        if not os.path.exists(posts_viewed_path):
            # If the file is missing, create a CSV with only headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        posts_viewed_data = load_json_data(posts_viewed_path)
        posts_viewed = process_posts_viewed_data(posts_viewed_data.get("impressions_history_posts_seen", []))
        daily_counts, weekly_counts = aggregate_counts(posts_viewed)
        write_to_csv(daily_counts, weekly_counts)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()