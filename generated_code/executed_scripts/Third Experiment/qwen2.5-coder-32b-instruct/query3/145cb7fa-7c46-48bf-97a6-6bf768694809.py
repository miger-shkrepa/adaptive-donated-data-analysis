import os
import csv
import json
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_week_number(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    week_number = date.isocalendar()[1]
    return f"Week {date.year}-{week_number:02}"

def process_posts_viewed(file_path):
    daily_posts = {}
    weekly_posts = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data.get('impressions_history_posts_seen', []):
                string_map_data = entry.get('string_map_data', {})
                time_data = string_map_data.get('Time', {})
                timestamp = time_data.get('timestamp', 0)
                if timestamp:
                    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    if date not in daily_posts:
                        daily_posts[date] = 0
                    daily_posts[date] += 1
                    week = get_week_number(date)
                    if week not in weekly_posts:
                        weekly_posts[week] = 0
                    weekly_posts[week] += 1
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The posts_viewed.json file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the file: {str(e)}")

    return daily_posts, weekly_posts

def write_to_csv(daily_posts, weekly_posts):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

            for date, count in daily_posts.items():
                writer.writerow([date, count, 'Daily'])

            for week, count in weekly_posts.items():
                writer.writerow([week, count, 'Weekly'])
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to the CSV file: {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(posts_viewed_path):
            write_to_csv({}, {})
            return

        daily_posts, weekly_posts = process_posts_viewed(posts_viewed_path)
        write_to_csv(daily_posts, weekly_posts)

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()