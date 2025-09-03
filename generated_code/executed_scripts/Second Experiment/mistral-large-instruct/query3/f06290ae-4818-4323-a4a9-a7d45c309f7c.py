import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse JSON files and extract post view data
def parse_posts_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            posts_viewed = data.get('impressions_history_posts_seen', [])
            return posts_viewed
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to aggregate post views by day and week
def aggregate_post_views(posts_viewed):
    daily_views = {}
    weekly_views = {}

    for post in posts_viewed:
        timestamp = post['string_map_data']['Time']['timestamp']
        date = datetime.fromtimestamp(timestamp).date()
        week = date.isocalendar()
        week_str = f"Week {week[0]}-{week[1]:02d}"

        daily_views[date] = daily_views.get(date, 0) + 1
        weekly_views[week_str] = weekly_views.get(week_str, 0) + 1

    return daily_views, weekly_views

# Function to write the results to a CSV file
def write_to_csv(daily_views, weekly_views):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_views.items():
            writer.writerow({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_views.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to process the directory and generate the CSV
def main():
    posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

    try:
        posts_viewed = parse_posts_viewed(posts_viewed_file)
        daily_views, weekly_views = aggregate_post_views(posts_viewed)
        write_to_csv(daily_views, weekly_views)
    except Exception as e:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        print(e)

if __name__ == "__main__":
    main()