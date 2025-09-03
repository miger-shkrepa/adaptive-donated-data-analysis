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

def process_directory(root_dir):
    try:
        os.listdir(root_dir)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    results = []
    for filename in os.listdir(root_dir):
        file_path = os.path.join(root_dir, filename)
        if os.path.isfile(file_path):
            if filename == "directory_structure_final2.txt":
                data = process_json_file(file_path)
                for item in data['items']:
                    if 'creation_timestamp' in item and 'title' in item:
                        date = item['creation_timestamp']
                        if date % 7 == 0:
                            results.append([f"Week {date//7}-{(date//7)+1}", 1, 'Weekly'])
                        else:
                            results.append([datetime.fromtimestamp(date).strftime('%Y-%m-%d'), 1, 'Daily'])
            elif filename == "recently_viewed_items.json":
                data = process_json_file(file_path)
                for item in data['structure']['checkout_saved_recently_viewed_products']:
                    for key, value in item['string_map_data'].items():
                        results.append([datetime.now().strftime('%Y-%m-%d'), 1, 'Daily'])
            elif filename == "story_likes.json":
                data = process_json_file(file_path)
                for item in data['structure']['story_activities_story_likes']:
                    for item in item['string_list_data']:
                        results.append([datetime.now().strftime('%Y-%m-%d'), 1, 'Daily'])
            elif filename == "emoji_sliders.json":
                data = process_json_file(file_path)
                for item in data['structure']['story_activities_emoji_sliders']:
                    for item in item['string_list_data']:
                        results.append([datetime.now().strftime('%Y-%m-%d'), 1, 'Daily'])
            elif filename == "polls.json":
                data = process_json_file(file_path)
                for item in data['structure']['story_activities_polls']:
                    for item in item['string_list_data']:
                        results.append([datetime.now().strftime('%Y-%m-%d'), 1, 'Daily'])
            elif filename == "questions.json":
                data = process_json_file(file_path)
                for item in data['structure']['story_activities_questions']:
                    for item in item['string_list_data']:
                        results.append([datetime.now().strftime('%Y-%m-%d'), 1, 'Daily'])
            elif filename == "quizzes.json":
                data = process_json_file(file_path)
                for item in data['structure']['story_activities_quizzes']:
                    for item in item['string_list_data']:
                        results.append([datetime.now().strftime('%Y-%m-%d'), 1, 'Daily'])
        else:
            process_directory(file_path)

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for result in results:
            writer.writerow(result)

root_dir = "root_dir"
process_directory(root_dir)