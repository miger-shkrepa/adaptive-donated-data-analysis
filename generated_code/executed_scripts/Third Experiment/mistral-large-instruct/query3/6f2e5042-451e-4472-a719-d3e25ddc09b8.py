import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to parse the JSON files and extract the required data
def parse_posts_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            posts_viewed = data.get('impressions_history_posts_seen', [])
            return posts_viewed
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to aggregate the data into daily and weekly counts
def aggregate_data(posts_viewed):
    daily_counts = {}
    weekly_counts = {}

    for post in posts_viewed:
        timestamp = post['string_map_data']['Time']['timestamp']
        date = datetime.fromtimestamp(timestamp).date()
        week = date.isocalendar()[:2]
        week_str = f"Week {week[0]}-{week[1]:02d}"

        daily_counts[date] = daily_counts.get(date, 0) + 1
        weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1

    return daily_counts, weekly_counts

# Function to write the aggregated data to a CSV file
def write_to_csv(daily_counts, weekly_counts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for date, count in daily_counts.items():
                writer.writerow({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': count, 'Type': 'Daily'})

            for week, count in weekly_counts.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Main function to process the data
def main():
    posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    posts_viewed = parse_posts_viewed(posts_viewed_file)
    daily_counts, weekly_counts = aggregate_data(posts_viewed)
    write_to_csv(daily_counts, weekly_counts)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)