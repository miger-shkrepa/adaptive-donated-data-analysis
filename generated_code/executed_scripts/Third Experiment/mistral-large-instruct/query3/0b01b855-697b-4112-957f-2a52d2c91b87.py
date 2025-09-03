import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Function to parse JSON files and extract post view data
def parse_posts_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            posts_viewed = []
            for entry in data.get('impressions_history_posts_seen', []):
                timestamp = entry['string_map_data'].get('Time', {}).get('timestamp')
                if timestamp:
                    date = datetime.fromtimestamp(timestamp)
                    posts_viewed.append(date)
            return posts_viewed
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

# Function to aggregate post views by day and week
def aggregate_post_views(posts_viewed):
    daily_views = {}
    weekly_views = {}

    for date in posts_viewed:
        date_str = date.strftime('%Y-%m-%d')
        week_str = f"Week {date.strftime('%Y-%W')}"

        daily_views[date_str] = daily_views.get(date_str, 0) + 1
        weekly_views[week_str] = weekly_views.get(week_str, 0) + 1

    return daily_views, weekly_views

# Function to write the results to a CSV file
def write_to_csv(daily_views, weekly_views):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_views.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_views.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to process the data
def main():
    try:
        posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        posts_viewed = parse_posts_viewed(posts_viewed_file)

        daily_views, weekly_views = aggregate_post_views(posts_viewed)

        write_to_csv(daily_views, weekly_views)

    except FileNotFoundError as e:
        print(e)
        # Write only the headers to the CSV file if the necessary file is missing
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()