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
            posts_viewed = []
            for entry in data.get('impressions_history_posts_seen', []):
                timestamp = entry['string_map_data']['Time']['timestamp']
                date = datetime.fromtimestamp(timestamp)
                posts_viewed.append(date)
            return posts_viewed
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to aggregate post views by day and week
def aggregate_post_views(posts_viewed):
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

# Function to write the results to a CSV file
def write_to_csv(daily_counts, weekly_counts):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for date, count in daily_counts.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

            for week, count in weekly_counts.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})
    except Exception as e:
        raise ValueError(f"Error: ValueError: Failed to write to CSV file. {str(e)}")

# Main function to process the directory and generate the CSV file
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    posts_viewed = []

    if os.path.exists(posts_viewed_file):
        posts_viewed = parse_posts_viewed(posts_viewed_file)

    daily_counts, weekly_counts = aggregate_post_views(posts_viewed)
    write_to_csv(daily_counts, weekly_counts)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)