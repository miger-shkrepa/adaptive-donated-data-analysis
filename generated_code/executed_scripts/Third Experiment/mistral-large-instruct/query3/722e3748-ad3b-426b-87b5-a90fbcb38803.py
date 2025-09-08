import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to parse the JSON files and extract the required data
def parse_json_files(directory):
    posts_viewed_data = []

    # Check if the directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Iterate through the directory to find the relevant JSON files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "posts_viewed.json":
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for entry in data.get("impressions_history_posts_seen", []):
                        timestamp = entry["string_map_data"]["Time"]["timestamp"]
                        date = datetime.fromtimestamp(timestamp)
                        posts_viewed_data.append(date)

    return posts_viewed_data

# Function to aggregate the data into daily and weekly counts
def aggregate_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}

    for date in posts_viewed_data:
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

# Function to write the aggregated data to a CSV file
def write_to_csv(daily_counts, weekly_counts):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to execute the script
def main():
    try:
        posts_viewed_data = parse_json_files(root_dir)
        daily_counts, weekly_counts = aggregate_data(posts_viewed_data)
        write_to_csv(daily_counts, weekly_counts)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()