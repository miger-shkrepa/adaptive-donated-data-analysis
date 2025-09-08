import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    try:
        posts_viewed_daily = {}
        posts_viewed_weekly = {}

        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate over all files in the directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "posts_viewed.json":
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r') as file:
                            # Since the structure of posts_viewed.json is not provided, 
                            # we assume it contains a list of dictionaries with 'Time' key
                            import json
                            data = json.load(file)
                            for post in data['impressions_history_posts_seen']:
                                time = post['string_map_data']['Time']['timestamp']
                                date = datetime.fromtimestamp(time)
                                date_str = date.strftime('%Y-%m-%d')
                                week_str = date.strftime('Week %Y-%W')

                                # Update daily count
                                if date_str in posts_viewed_daily:
                                    posts_viewed_daily[date_str] += 1
                                else:
                                    posts_viewed_daily[date_str] = 1

                                # Update weekly count
                                if week_str in posts_viewed_weekly:
                                    posts_viewed_weekly[week_str] += 1
                                else:
                                    posts_viewed_weekly[week_str] = 1
                    except Exception as e:
                        print(f"Error reading {file_path}: {str(e)}")

        return posts_viewed_daily, posts_viewed_weekly

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(posts_viewed_daily, posts_viewed_weekly):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for date, count in posts_viewed_daily.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

            for week, count in posts_viewed_weekly.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        posts_viewed_daily, posts_viewed_weekly = get_posts_viewed(root_dir)
        write_to_csv(posts_viewed_daily, posts_viewed_weekly)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        print(e)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()