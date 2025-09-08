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
        date = datetime.strptime(item['string_map_data']['Merchant Name']['value'], '%Y-%m-%d')
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
                date = datetime.fromtimestamp(item['string_list_data'][0]['timestamp'])
                if date.weekday() < 5:  # Monday to Friday
                    result.append({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': 1, 'Type': 'Daily'})
                else:
                    result.append({'Date/Week': f'Week {date.strftime("%Y-%W")}', 'Posts Viewed': 1, 'Type': 'Weekly'})
    return result

def main():
    root_dir = "root_dir"
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    result = []
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)
        if os.path.isfile(file_path):
            if file.endswith('.json'):
                data = process_json_file(file_path)
                result.extend(process_shopping_data(data))
                result.extend(process_story_sticker_interactions(data))

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Date/Week', 'Posts Viewed', 'Type'])
        writer.writeheader()
        writer.writerows(result)

if __name__ == "__main__":
    main()