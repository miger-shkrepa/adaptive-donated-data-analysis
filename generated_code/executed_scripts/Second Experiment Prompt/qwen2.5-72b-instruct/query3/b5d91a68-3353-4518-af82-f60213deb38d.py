import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to load JSON data from a file
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to process posts viewed data
def process_posts_viewed(posts_viewed_data):
    posts_viewed = []
    for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
        for data in entry.get("string_map_data", {}).get("Time", []):
            timestamp = data.get("timestamp")
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

# Main function to execute the query
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(posts_viewed_path):
            write_to_csv({}, {})
            return

        posts_viewed_data = load_json(posts_viewed_path)
        posts_viewed = process_posts_viewed(posts_viewed_data)
        daily_counts, weekly_counts = aggregate_counts(posts_viewed)
        write_to_csv(daily_counts, weekly_counts)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()