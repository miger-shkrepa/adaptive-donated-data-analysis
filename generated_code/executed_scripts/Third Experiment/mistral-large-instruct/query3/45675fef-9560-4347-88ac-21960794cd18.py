import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to parse JSON files and extract data
def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to process the directory and extract posts viewed data
def process_directory(root_dir):
    posts_viewed_data = []

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Path to the posts_viewed.json file
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

    # Check if the posts_viewed.json file exists
    if os.path.exists(posts_viewed_path):
        posts_viewed_data = parse_json_file(posts_viewed_path)

    return posts_viewed_data

# Function to aggregate posts viewed data
def aggregate_posts_viewed_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}

    for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
        timestamp = entry["string_map_data"]["Time"]["timestamp"]
        date = datetime.fromtimestamp(timestamp)
        date_str = date.strftime('%Y-%m-%d')
        week_str = f"Week {date.strftime('%Y-%W')}"

        # Increment daily count
        if date_str in daily_counts:
            daily_counts[date_str] += 1
        else:
            daily_counts[date_str] = 1

        # Increment weekly count
        if week_str in weekly_counts:
            weekly_counts[week_str] += 1
        else:
            weekly_counts[week_str] = 1

    return daily_counts, weekly_counts

# Function to write the results to a CSV file
def write_to_csv(daily_counts, weekly_counts):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Write daily counts
        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        # Write weekly counts
        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to execute the script
def main():
    try:
        posts_viewed_data = process_directory(root_dir)
        daily_counts, weekly_counts = aggregate_posts_viewed_data(posts_viewed_data)
        write_to_csv(daily_counts, weekly_counts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()