import csv
import os
import json
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
    daily_posts_dir = os.path.join(root_dir, 'your_activity_across_facebook', 'content')
    if os.path.exists(daily_posts_dir):
        for date in os.listdir(daily_posts_dir):
            if date.startswith('posts_'):
                date_str = date.split('_')[1]
                date_obj = datetime.datetime.strptime(date_str, '%Y%m%d')
                if date_obj.weekday() == 0:  # Monday
                    week_str = date_obj.strftime('%Y-%W')
                    posts_viewed = 0
                    try:
                        with open(os.path.join(daily_posts_dir, date), 'r') as f:
                            data = json.load(f)
                            posts_viewed = len(data)
                    except FileNotFoundError:
                        pass
                    writer.writerow([week_str, posts_viewed, 'Weekly'])
                else:
                    writer.writerow([date_obj.strftime('%Y-%m-%d'), posts_viewed, 'Daily'])
    else:
        writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

    # Iterate over the weekly posts
    weekly_posts_dir = os.path.join(root_dir, 'your_activity_across_facebook', 'content')
    if os.path.exists(weekly_posts_dir):
        for week in os.listdir(weekly_posts_dir):
            if week.startswith('profile_photos'):
                week_str = week.split('_')[0]
                week_obj = datetime.datetime.strptime(week_str, '%Y')
                posts_viewed = 0
                try:
                    with open(os.path.join(weekly_posts_dir, week), 'r') as f:
                        data = json.load(f)
                        posts_viewed = len(data['ig_profile_picture'])
                except FileNotFoundError:
                    pass
                writer.writerow([week_obj.strftime('%Y-%W'), posts_viewed, 'Weekly'])
    else:
        writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])