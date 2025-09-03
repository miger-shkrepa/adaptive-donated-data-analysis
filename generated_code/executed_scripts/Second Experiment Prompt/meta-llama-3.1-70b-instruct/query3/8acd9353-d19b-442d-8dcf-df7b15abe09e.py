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

        # Iterate over the files in the 'ads_information' directory
        ads_info_dir = os.path.join(root_dir, 'ads_information', 'ads_and_topics')
        if os.path.exists(ads_info_dir):
            for filename in os.listdir(ads_info_dir):
                if filename == 'posts_viewed.json':
                    posts_viewed_file = os.path.join(ads_info_dir, filename)
                    if os.path.exists(posts_viewed_file):
                        with open(posts_viewed_file, 'r') as file:
                            # Since the exact structure of the JSON file is not provided, 
                            # we assume it's a list of dictionaries with 'Time' and 'Author' keys
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

        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for date, count in daily_posts_viewed.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
            for week, count in weekly_posts_viewed.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

get_posts_viewed(root_dir)