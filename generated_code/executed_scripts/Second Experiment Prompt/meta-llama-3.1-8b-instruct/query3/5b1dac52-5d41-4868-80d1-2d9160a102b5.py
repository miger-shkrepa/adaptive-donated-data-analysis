import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

    # Iterate over the daily and weekly posts
    for date in os.listdir(os.path.join(root_dir, 'media', 'posts')):
        if date.startswith('2023'):
            # Get the date and week
            date_obj = datetime.datetime.strptime(date, '%Y%m')
            date_str = date_obj.strftime('%Y-%m-%d')
            week_str = date_obj.strftime('%Y-%W')

            # Initialize the posts viewed count
            posts_viewed = 0

            # Check if the daily posts file exists
            daily_posts_file = os.path.join(root_dir, 'media', 'posts', date)
            if os.path.exists(daily_posts_file):
                try:
                    # Open the daily posts file
                    with open(daily_posts_file, 'r') as daily_posts:
                        # Read the daily posts file
                        for line in daily_posts:
                            # Check if the line contains a post
                            if 'post' in line:
                                # Increment the posts viewed count
                                posts_viewed += 1
                except PermissionError:
                    # If a permission error occurs, skip this file
                    continue

            # Check if the weekly posts file exists
            weekly_posts_file = os.path.join(root_dir, 'media', 'posts', week_str)
            if os.path.exists(weekly_posts_file):
                try:
                    # Open the weekly posts file
                    with open(weekly_posts_file, 'r') as weekly_posts:
                        # Read the weekly posts file
                        for line in weekly_posts:
                            # Check if the line contains a post
                            if 'post' in line:
                                # Increment the posts viewed count
                                posts_viewed += 1
                except PermissionError:
                    # If a permission error occurs, skip this file
                    continue

            # Write the result to the CSV file
            writer.writerow([date_str, posts_viewed, 'Daily'])
            writer.writerow([week_str, posts_viewed, 'Weekly'])