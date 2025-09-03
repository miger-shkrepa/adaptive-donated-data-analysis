import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def get_login_devices(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize result list
        result = []

        # Iterate through 'your_instagram_activity' directory
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(activity_dir):
            media_dir = os.path.join(activity_dir, 'media')
            if os.path.exists(media_dir):
                posts_dir = os.path.join(media_dir, 'posts_1.json')
                if os.path.exists(posts_dir):
                    with open(posts_dir, 'r') as f:
                        data = json.load(f)
                        for post in data:
                            for media in post['media']:
                                if 'media_metadata' in media:
                                    if 'photo_metadata' in media['media_metadata']:
                                        if 'exif_data' in media['media_metadata']['photo_metadata']:
                                            for exif in media['media_metadata']['photo_metadata']['exif_data']:
                                                if 'device_id' in exif:
                                                    device_id = exif['device_id']
                                                    if 'date_time_original' in exif:
                                                        login_time = datetime.strptime(exif['date_time_original'], '%Y:%m:%d %H:%M:%S')
                                                        result.append((device_id, login_time.strftime('%Y-%m-%d %H:%M:%S')))

        # Write result to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])  # header
            writer.writerows(result)

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise ValueError("Error: " + str(e))

get_login_devices(root_dir)