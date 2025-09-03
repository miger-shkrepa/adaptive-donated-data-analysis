import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to parse the JSON file and extract posts viewed data
def parse_posts_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            posts_viewed = []
            for entry in data.get("impressions_history_posts_seen", []):
                timestamp = entry.get("string_map_data", {}).get("Time", {}).get("timestamp", 0)
                if timestamp:
                    date = datetime.fromtimestamp(timestamp)
                    posts_viewed.append(date)
            return posts_viewed
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

# Function to aggregate posts viewed data
def aggregate_posts_viewed(posts_viewed):
    daily_count = {}
    weekly_count = {}

    for date in posts_viewed:
        date_str = date.strftime('%Y-%m-%d')
        week_str = f"Week {date.strftime('%Y-%W')}"

        if date_str in daily_count:
            daily_count[date_str] += 1
        else:
            daily_count[date_str] = 1

        if week_str in weekly_count:
            weekly_count[week_str] += 1
        else:
            weekly_count[week_str] = 1

    return daily_count, weekly_count

# Function to write the results to a CSV file
def write_to_csv(daily_count, weekly_count):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for date, count in daily_count.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

            for week, count in weekly_count.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})
    except Exception as e:
        raise IOError(f"IOError: Failed to write to CSV file. {str(e)}")

# Main function to process the data
def main():
    posts_viewed_file = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    posts_viewed = parse_posts_viewed(posts_viewed_file)
    daily_count, weekly_count = aggregate_posts_viewed(posts_viewed)
    write_to_csv(daily_count, weekly_count)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")