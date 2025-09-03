import os
import csv
import json
from datetime import datetime

root_dir = "root_dir"

def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data.get('story_activities_questions', []) + \
                  data.get('story_activities_polls', []) + \
                  data.get('story_activities_emoji_sliders', []) + \
                  data.get('story_activities_quizzes', []):
            for entry in item.get('string_list_data', []):
                timestamp = entry.get('timestamp')
                if timestamp:
                    device_id = item.get('media_metadata', {}).get('photo_metadata', {}).get('exif_data', [{}])[0].get('device_id', '')
                    if not device_id:
                        device_id = item.get('media_metadata', {}).get('video_metadata', {}).get('exif_data', [{}])[0].get('device_id', '')
                    if device_id:
                        login_time = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
                        yield device_id, login_time

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.isdir(root_dir):
        raise ValueError("ValueError: The root directory is not a valid directory.")
    
    results = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    results.extend(process_json_file(file_path))
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device ID', 'Login Time'])
        writer.writerows(results)

if __name__ == "__main__":
    main()