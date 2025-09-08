import os
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_posts_viewed_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = eval(file.read())
            return data['impressions_history_posts_seen']
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while reading the posts_viewed.json file - {str(e)}")

def convert_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def calculate_daily_and_weekly_views(posts_viewed_data):
    daily_views = {}
    weekly_views = {}

    for post in posts_viewed_data:
        timestamp = post['string_map_data']['Time']['timestamp']
        date = convert_timestamp_to_date(timestamp)
        week = datetime.fromtimestamp(timestamp).strftime('Week %Y-%U')

        if date in daily_views:
            daily_views[date] += 1
        else:
            daily_views[date] = 1

        if week in weekly_views:
            weekly_views[week] += 1
        else:
            weekly_views[week] = 1

    return daily_views, weekly_views

def write_to_csv(daily_views, weekly_views, output_path):
    try:
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

            for date, count in daily_views.items():
                writer.writerow([date, count, 'Daily'])

            for week, count in weekly_views.items():
                writer.writerow([week, count, 'Weekly'])
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while writing to the CSV file - {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        posts_viewed_file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        posts_viewed_data = get_posts_viewed_data(posts_viewed_file_path)

        daily_views, weekly_views = calculate_daily_and_weekly_views(posts_viewed_data)

        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        write_to_csv(daily_views, weekly_views, output_path)

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()