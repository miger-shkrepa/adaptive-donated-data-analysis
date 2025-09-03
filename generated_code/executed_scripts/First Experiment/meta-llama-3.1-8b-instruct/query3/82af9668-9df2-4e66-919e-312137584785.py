import os
import csv
import json
from datetime import datetime, timedelta

def process_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        raise ValueError("Error: Invalid JSON format in file: " + file_path)

def process_shopping_data(data):
    result = []
    for item in data['shopping']['recently_viewed_items.json']['structure']['checkout_saved_recently_viewed_products']:
        date = datetime.strptime(item['string_map_data']['Product Name']['value'], '%Y-%m-%d')
        if date.weekday() < 5:
            result.append((date.strftime('%Y-%m-%d'), 1, 'Daily'))
        else:
            result.append((date.strftime('%Y-%m-%d'), 1, 'Weekly'))
    return result

def process_story_sticker_interactions(data):
    result = []
    for file in data['story_sticker_interactions'].values():
        for item in file['structure']['story_activities_emoji_sliders']:
            for timestamp in item['string_list_data']:
                date = datetime.fromtimestamp(timestamp['timestamp'])
                if date.weekday() < 5:
                    result.append((date.strftime('%Y-%m-%d'), 1, 'Daily'))
                else:
                    result.append((date.strftime('%Y-%m-%d'), 1, 'Weekly'))
    return result

def process_events(data):
    result = []
    for file in data['events'].values():
        if file is not None:
            for item in file:
                date = datetime.strptime(item['date_time_original'], '%Y-%m-%d %H:%M:%S')
                if date.weekday() < 5:
                    result.append((date.strftime('%Y-%m-%d'), 1, 'Daily'))
                else:
                    result.append((date.strftime('%Y-%m-%d'), 1, 'Weekly'))
    return result

def process_video_metadata(data):
    result = []
    for item in data['media_metadata']['video_metadata']['exif_data']:
        date = datetime.strptime(item['date_time_original'], '%Y-%m-%d %H:%M:%S')
        if date.weekday() < 5:
            result.append((date.strftime('%Y-%m-%d'), 1, 'Daily'))
        else:
            result.append((date.strftime('%Y-%m-%d'), 1, 'Weekly'))
    return result

def process_photo_metadata(data):
    result = []
    for item in data['media_metadata']['photo_metadata']['exif_data']:
        date = datetime.strptime(item['date_time_original'], '%Y-%m-%d %H:%M:%S')
        if date.weekday() < 5:
            result.append((date.strftime('%Y-%m-%d'), 1, 'Daily'))
        else:
            result.append((date.strftime('%Y-%m-%d'), 1, 'Weekly'))
    return result

def process_data(root_dir):
    result = []
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)
        if os.path.isfile(file_path):
            if file.endswith('.json'):
                data = process_json_file(file_path)
                if 'shopping' in data:
                    result.extend(process_shopping_data(data))
                elif 'story_sticker_interactions' in data:
                    result.extend(process_story_sticker_interactions(data))
                elif 'events' in data:
                    result.extend(process_events(data))
                elif 'media_metadata' in data:
                    if 'video_metadata' in data['media_metadata']:
                        result.extend(process_video_metadata(data))
                    elif 'photo_metadata' in data['media_metadata']:
                        result.extend(process_photo_metadata(data))
    return result

def save_to_csv(data):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
        for item in data:
            writer.writerow(item)

if __name__ == "__main__":
    root_dir = "root_dir"
    try:
        data = process_data(root_dir)
        save_to_csv(data)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except ValueError as e:
        raise ValueError("Error: " + str(e))