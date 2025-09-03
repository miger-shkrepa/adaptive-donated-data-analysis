import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_post_views(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize variables to store post views
        daily_views = {}
        weekly_views = {}

        # Check if 'your_instagram_activity' directory exists
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(activity_dir):
            # Check if 'likes' directory exists
            likes_dir = os.path.join(activity_dir, 'likes')
            if os.path.exists(likes_dir):
                # Check if 'liked_posts.json' file exists
                liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
                if os.path.exists(liked_posts_file):
                    with open(liked_posts_file, 'r') as file:
                        liked_posts_data = json.load(file)
                        for post in liked_posts_data['likes_media_likes']:
                            for data in post['string_list_data']:
                                timestamp = data['timestamp']
                                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                                week = datetime.fromtimestamp(timestamp).strftime('Week %Y-%U')
                                if date not in daily_views:
                                    daily_views[date] = 1
                                else:
                                    daily_views[date] += 1
                                if week not in weekly_views:
                                    weekly_views[week] = 1
                                else:
                                    weekly_views[week] += 1

            # Check if 'saved' directory exists
            saved_dir = os.path.join(activity_dir, 'saved')
            if os.path.exists(saved_dir):
                # Check if 'saved_posts.json' file exists
                saved_posts_file = os.path.join(saved_dir, 'saved_posts.json')
                if os.path.exists(saved_posts_file):
                    with open(saved_posts_file, 'r') as file:
                        saved_posts_data = json.load(file)
                        for post in saved_posts_data['saved_saved_media']:
                            saved_on = post['string_map_data']['Saved on']
                            timestamp = saved_on['timestamp']
                            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                            week = datetime.fromtimestamp(timestamp).strftime('Week %Y-%U')
                            if date not in daily_views:
                                daily_views[date] = 1
                            else:
                                daily_views[date] += 1
                            if week not in weekly_views:
                                weekly_views[week] = 1
                            else:
                                weekly_views[week] += 1

        return daily_views, weekly_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(daily_views, weekly_views):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            for date, views in daily_views.items():
                writer.writerow([date, views, 'Daily'])
            for week, views in weekly_views.items():
                writer.writerow([week, views, 'Weekly'])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        daily_views, weekly_views = get_post_views(root_dir)
        write_to_csv(daily_views, weekly_views)

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except ValueError as e:
        raise ValueError("ValueError: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()