import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_post_views(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize variables to store post views
        daily_post_views = {}
        weekly_post_views = {}

        # Iterate over the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "posts_viewed.json":
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r') as file:
                            # Assuming the JSON file has the same structure as in the problem description
                            import json
                            data = json.load(file)
                            for post in data['impressions_history_posts_seen']:
                                time = post['string_map_data']['Time']['timestamp']
                                date = datetime.fromtimestamp(time)
                                date_str = date.strftime('%Y-%m-%d')
                                week_str = date.strftime('Week %Y-%W')
                                if date_str not in daily_post_views:
                                    daily_post_views[date_str] = 0
                                daily_post_views[date_str] += 1
                                if week_str not in weekly_post_views:
                                    weekly_post_views[week_str] = 0
                                weekly_post_views[week_str] += 1
                    except Exception as e:
                        print(f"Error reading file {file_path}: {str(e)}")

        return daily_post_views, weekly_post_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(daily_post_views, weekly_post_views):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for date, views in daily_post_views.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': views, 'Type': 'Daily'})
            for week, views in weekly_post_views.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': views, 'Type': 'Weekly'})
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        daily_post_views, weekly_post_views = get_post_views(root_dir)
        write_to_csv(daily_post_views, weekly_post_views)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        print(str(e))
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()