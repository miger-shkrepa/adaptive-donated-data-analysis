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

        # Iterate over the directories and files in the root directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                # Check if the file is 'posts_viewed.json'
                if filename == 'posts_viewed.json':
                    file_path = os.path.join(dirpath, filename)
                    try:
                        # Open the file and read its contents
                        with open(file_path, 'r') as file:
                            # Since the structure of the file is not provided, we assume it's a JSON file
                            # with a list of posts viewed, where each post has a 'Time' field with a timestamp
                            import json
                            data = json.load(file)
                            for post in data['impressions_history_posts_seen']:
                                timestamp = post['string_map_data']['Time']['timestamp']
                                date = datetime.fromtimestamp(timestamp)
                                date_str = date.strftime('%Y-%m-%d')
                                week_str = 'Week ' + date.strftime('%Y-%W')
                                if date_str not in daily_posts_viewed:
                                    daily_posts_viewed[date_str] = 0
                                daily_posts_viewed[date_str] += 1
                                if week_str not in weekly_posts_viewed:
                                    weekly_posts_viewed[week_str] = 0
                                weekly_posts_viewed[week_str] += 1
                    except Exception as e:
                        raise ValueError("ValueError: Failed to read 'posts_viewed.json' file. " + str(e))

        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for date, count in daily_posts_viewed.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
            for week, count in weekly_posts_viewed.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

    except Exception as e:
        # If an error occurs, write a CSV file with only the column headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise ValueError("ValueError: " + str(e))

get_posts_viewed(root_dir)