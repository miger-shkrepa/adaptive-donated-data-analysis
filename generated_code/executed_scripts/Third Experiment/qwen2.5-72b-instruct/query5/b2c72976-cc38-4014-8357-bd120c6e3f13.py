import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def process_data():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        device_login_times = []

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if 'media_metadata' in data and 'photo_metadata' in data['media_metadata']:
                            exif_data = data['media_metadata']['photo_metadata'].get('exif_data', [])
                            for entry in exif_data:
                                device_id = entry.get('device_id')
                                date_time_original = entry.get('date_time_original')
                                if device_id and date_time_original:
                                    try:
                                        login_time = datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S')
                                        device_login_times.append((device_id, login_time.strftime('%Y-%m-%d %H:%M:%S')))
                                    except ValueError:
                                        raise ValueError("Error: Invalid date format in exif_data.")

        if not device_login_times:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device ID', 'Login Time'])
        else:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Device ID', 'Login Time'])
                writer.writerows(device_login_times)

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Error: {str(e)}")

process_data()