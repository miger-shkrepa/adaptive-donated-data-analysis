import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_login_time(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize lists to store device IDs and login times
        device_ids = []
        login_times = []

        # Check if 'your_instagram_activity' directory exists
        instagram_activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(instagram_activity_dir):
            # Check if 'likes' directory exists
            likes_dir = os.path.join(instagram_activity_dir, 'likes')
            if os.path.exists(likes_dir):
                # Check if 'liked_posts.json' file exists
                liked_posts_file = os.path.join(likes_dir, 'liked_posts.json')
                if os.path.exists(liked_posts_file):
                    with open(liked_posts_file, 'r') as file:
                        data = json.load(file)
                        for likes_media_likes in data['likes_media_likes']:
                            for string_list_data in likes_media_likes['string_list_data']:
                                # Assuming 'href' is the device ID and 'timestamp' is the login time
                                device_id = string_list_data['href']
                                timestamp = string_list_data['timestamp']
                                login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                                device_ids.append(device_id)
                                login_times.append(login_time)

            # Check if 'saved' directory exists
            saved_dir = os.path.join(instagram_activity_dir, 'saved')
            if os.path.exists(saved_dir):
                # Check if 'saved_posts.json' file exists
                saved_posts_file = os.path.join(saved_dir, 'saved_posts.json')
                if os.path.exists(saved_posts_file):
                    with open(saved_posts_file, 'r') as file:
                        data = json.load(file)
                        for saved_saved_media in data['saved_saved_media']:
                            string_map_data = saved_saved_media['string_map_data']
                            if 'Saved on' in string_map_data:
                                # Assuming 'href' is the device ID and 'timestamp' is the login time
                                device_id = string_map_data['Saved on']['href']
                                timestamp = string_map_data['Saved on']['timestamp']
                                login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                                device_ids.append(device_id)
                                login_times.append(login_time)

        # Write to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Device ID', 'Login Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device_id, login_time in zip(device_ids, login_times):
                writer.writerow({'Device ID': device_id, 'Login Time': login_time})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: {e}")
    except Exception as e:
        raise ValueError(f"ValueError: {e}")

get_login_time(root_dir)