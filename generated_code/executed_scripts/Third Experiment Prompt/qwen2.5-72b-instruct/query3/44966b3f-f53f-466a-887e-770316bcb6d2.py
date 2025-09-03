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
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

# Function to get daily and weekly post views
def get_post_views(data):
    daily_views = {}
    weekly_views = {}

    try:
        for entry in data['impressions_history_posts_seen']:
            string_map_data = entry.get('string_map_data', {})
            time_str = string_map_data.get('Time', {}).get('timestamp')
            if time_str:
                time = int(time_str)
                date = datetime.fromtimestamp(time).date()
                week = date.strftime('%Y-%W')
                daily_views[date] = daily_views.get(date, 0) + 1
                weekly_views[week] = weekly_views.get(week, 0) + 1
    except KeyError as e:
        raise KeyError(f"Error: Missing key in JSON data: {e}")

    return daily_views, weekly_views

# Function to write results to CSV
def write_to_csv(daily_views, weekly_views):
    try:
        os.makedirs('query_responses', exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for date, count in daily_views.items():
                writer.writerow({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': count, 'Type': 'Daily'})

            for week, count in weekly_views.items():
                writer.writerow({'Date/Week': f"Week {week}", 'Posts Viewed': count, 'Type': 'Weekly'})
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file: {e}")

# Main function to process the data
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(posts_viewed_path):
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        data = load_json_data(posts_viewed_path)
        daily_views, weekly_views = get_post_views(data)
        write_to_csv(daily_views, weekly_views)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()