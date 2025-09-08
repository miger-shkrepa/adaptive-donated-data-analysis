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
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to process posts viewed data
def process_posts_viewed_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}

    for post in posts_viewed_data.get("impressions_history_posts_seen", []):
        string_map_data = post.get("string_map_data", {})
        timestamp = string_map_data.get("Time", {}).get("timestamp")
        if timestamp is not None:
            date = datetime.fromtimestamp(timestamp)
            date_str = date.strftime('%Y-%m-%d')
            week_str = f"Week {date.strftime('%Y-%W')}"

            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
            weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1

    return daily_counts, weekly_counts

# Function to generate the CSV file
def generate_csv(daily_counts, weekly_counts):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
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

        posts_viewed_file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(posts_viewed_file_path):
            generate_csv({}, {})
            return

        posts_viewed_data = load_json_data(posts_viewed_file_path)
        daily_counts, weekly_counts = process_posts_viewed_data(posts_viewed_data)
        generate_csv(daily_counts, weekly_counts)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()