import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to load JSON data from a file
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from the specified file.")

# Function to process posts data and generate daily and weekly counts
def process_posts_data(posts_data):
    daily_counts = {}
    weekly_counts = {}

    for post in posts_data:
        creation_timestamp = post.get('creation_timestamp')
        if creation_timestamp:
            date = datetime.fromtimestamp(creation_timestamp)
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

# Main function to process the directory and generate the CSV
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        daily_counts = {}
        weekly_counts = {}

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    data = load_json(file_path)

                    if 'posts' in file_path and 'media' in file_path:
                        if isinstance(data, list):
                            posts_data = data
                        elif isinstance(data, dict):
                            posts_data = data.get('ig_reels_media', []) + data.get('ig_stories', []) + data.get('ig_profile_picture', [])
                        else:
                            continue

                        daily, weekly = process_posts_data(posts_data)
                        daily_counts.update(daily)
                        weekly_counts.update(weekly)

        generate_csv(daily_counts, weekly_counts)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()