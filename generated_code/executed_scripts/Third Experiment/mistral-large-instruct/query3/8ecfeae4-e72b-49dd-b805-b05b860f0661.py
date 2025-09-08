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

# Function to parse the JSON file and extract posts viewed data
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

# Function to aggregate posts viewed data
def aggregate_posts_viewed(posts_viewed):
    daily_counts = {}
    weekly_counts = {}

    for post in posts_viewed:
        timestamp = post['string_map_data']['Time']['timestamp']
        date = datetime.fromtimestamp(timestamp)
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

# Function to write the results to a CSV file
def write_to_csv(daily_counts, weekly_counts):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to process the data
def main():
    posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    if not os.path.exists(posts_viewed_file):
        # If the file does not exist, create a CSV with only the column headers
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        return

    posts_viewed = parse_posts_viewed(posts_viewed_file)
    daily_counts, weekly_counts = aggregate_posts_viewed(posts_viewed)
    write_to_csv(daily_counts, weekly_counts)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)