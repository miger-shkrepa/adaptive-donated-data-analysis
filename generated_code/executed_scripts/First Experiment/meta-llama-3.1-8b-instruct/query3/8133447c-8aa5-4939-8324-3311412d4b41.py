import os
import csv
import json
from datetime import datetime, timedelta

def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as e:
        raise ValueError("Error: Invalid JSON format in file: " + file_path)

def process_shopping_data(data):
    result = []
    for item in data['shopping']['recently_viewed_items.json']['structure']['checkout_saved_recently_viewed_products']:
        date = datetime.strptime(item['string_map_data']['Date']['value'], '%Y-%m-%d')
        if date.weekday() < 5:  # Monday to Friday
            result.append({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': 1, 'Type': 'Daily'})
        else:
            result.append({'Date/Week': f'Week {date.strftime("%Y-%W")}', 'Posts Viewed': 1, 'Type': 'Weekly'})
    return result

def process_story_sticker_interactions(data):
    result = []
    for file in data['story_sticker_interactions'].values():
        if file['type'] == 'json':
            for item in file['structure']['story_activities_emoji_sliders']:
                date = datetime.strptime(item['title'], '%Y-%m-%d')
                if date.weekday() < 5:  # Monday to Friday
                    result.append({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': 1, 'Type': 'Daily'})
                else:
                    result.append({'Date/Week': f'Week {date.strftime("%Y-%W")}', 'Posts Viewed': 1, 'Type': 'Weekly'})
    return result

def process_all_data(root_dir):
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
    return result

def save_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Date/Week', 'Posts Viewed', 'Type'])
        writer.writeheader()
        writer.writerows(data)

def main():
    root_dir = "root_dir"
    try:
        data = process_all_data(root_dir)
        save_to_csv(data, 'query_responses/results.csv')
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()