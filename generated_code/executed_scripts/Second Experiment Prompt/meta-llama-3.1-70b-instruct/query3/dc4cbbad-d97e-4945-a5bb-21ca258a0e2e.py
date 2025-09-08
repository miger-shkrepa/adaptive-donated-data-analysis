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

        # Iterate over the 'ads_information' directory
        ads_info_dir = os.path.join(root_dir, 'ads_information', 'ads_and_topics')
        if os.path.exists(ads_info_dir):
            # Open the 'posts_viewed.json' file
            posts_viewed_file = os.path.join(ads_info_dir, 'posts_viewed.json')
            if os.path.exists(posts_viewed_file):
                with open(posts_viewed_file, 'r') as file:
                    # Read the JSON file
                    import json
                    data = json.load(file)
                    for post in data['impressions_history_posts_seen']:
                        # Get the timestamp of the post
                        timestamp = post['string_map_data']['Time']['timestamp']
                        date = datetime.fromtimestamp(timestamp)

                        # Update the daily posts viewed
                        date_str = date.strftime('%Y-%m-%d')
                        if date_str in daily_posts_viewed:
                            daily_posts_viewed[date_str] += 1
                        else:
                            daily_posts_viewed[date_str] = 1

                        # Update the weekly posts viewed
                        week_str = 'Week ' + date.strftime('%Y-%W')
                        if week_str in weekly_posts_viewed:
                            weekly_posts_viewed[week_str] += 1
                        else:
                            weekly_posts_viewed[week_str] = 1

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