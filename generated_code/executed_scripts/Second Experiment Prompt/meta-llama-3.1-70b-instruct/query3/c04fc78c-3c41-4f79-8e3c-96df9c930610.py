import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize variables to store the posts viewed
        daily_posts_viewed = {}
        weekly_posts_viewed = {}

        # Iterate over the directories and files
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "posts_viewed.json":
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r') as file:
                            # Read the JSON file
                            import json
                            data = json.load(file)
                            for post in data['impressions_history_posts_seen']:
                                time = post['string_map_data']['Time']['timestamp']
                                date = datetime.fromtimestamp(time)
                                date_str = date.strftime('%Y-%m-%d')
                                week_str = date.strftime('Week %Y-%W')
                                if date_str not in daily_posts_viewed:
                                    daily_posts_viewed[date_str] = 0
                                daily_posts_viewed[date_str] += 1
                                if week_str not in weekly_posts_viewed:
                                    weekly_posts_viewed[week_str] = 0
                                weekly_posts_viewed[week_str] += 1
                    except Exception as e:
                        raise ValueError("ValueError: Error reading the posts_viewed.json file: " + str(e))

        return daily_posts_viewed, weekly_posts_viewed

    except Exception as e:
        raise Exception("Error: " + str(e))

def write_to_csv(daily_posts_viewed, weekly_posts_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            for date, posts in daily_posts_viewed.items():
                writer.writerow([date, posts, "Daily"])
            for week, posts in weekly_posts_viewed.items():
                writer.writerow([week, posts, "Weekly"])
    except Exception as e:
        raise Exception("Error: " + str(e))

def main():
    try:
        daily_posts_viewed, weekly_posts_viewed = get_posts_viewed(root_dir)
        write_to_csv(daily_posts_viewed, weekly_posts_viewed)
    except FileNotFoundError:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()