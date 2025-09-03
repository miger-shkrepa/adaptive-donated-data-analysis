import os
import csv
import json
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_posts_viewed_frequency():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        daily_views = {}
        weekly_views = {}

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'messages' in data:
                            for message in data['messages']:
                                timestamp_ms = message.get('timestamp_ms')
                                if timestamp_ms:
                                    date = datetime.fromtimestamp(timestamp_ms / 1000.0).date()
                                    week = date.strftime('Week %Y-%W')
                                    daily_views[date] = daily_views.get(date, 0) + 1
                                    weekly_views[week] = weekly_views.get(week, 0) + 1

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for date, count in daily_views.items():
                writer.writerow({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': count, 'Type': 'Daily'})

            for week, count in weekly_views.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding failed. {e}")
    except Exception as e:
        raise ValueError(f"Error: An unexpected error occurred. {e}")

get_posts_viewed_frequency()