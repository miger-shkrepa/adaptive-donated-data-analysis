import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_posts_viewed_frequency():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        posts_viewed_data = []
        posts_file_path = os.path.join(root_dir, "posts_1.json")
        if not os.path.exists(posts_file_path):
            return []

        with open(posts_file_path, 'r') as file:
            posts_data = json.load(file)

        for post in posts_data:
            creation_timestamp = post.get('creation_timestamp')
            if creation_timestamp is None:
                continue

            date = datetime.fromtimestamp(creation_timestamp)
            date_str = date.strftime('%Y-%m-%d')
            week_str = f"Week {date.strftime('%Y-%W')}"

            posts_viewed_data.append((date_str, 1, 'Daily'))
            posts_viewed_data.append((week_str, 1, 'Weekly'))

        return posts_viewed_data

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def aggregate_data(posts_viewed_data):
    daily_data = {}
    weekly_data = {}

    for date, count, type in posts_viewed_data:
        if type == 'Daily':
            if date in daily_data:
                daily_data[date] += count
            else:
                daily_data[date] = count
        elif type == 'Weekly':
            if date in weekly_data:
                weekly_data[date] += count
            else:
                weekly_data[date] = count

    return daily_data, weekly_data

def write_to_csv(daily_data, weekly_data):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for date, count in daily_data.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_data.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

def main():
    try:
        posts_viewed_data = get_posts_viewed_frequency()
        if not posts_viewed_data:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        daily_data, weekly_data = aggregate_data(posts_viewed_data)
        write_to_csv(daily_data, weekly_data)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()