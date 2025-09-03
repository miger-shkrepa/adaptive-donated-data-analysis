import csv
import os
import json
from datetime import datetime, timedelta

def process_directory(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise e

    data = {}
    for filename in os.listdir(root_dir):
        file_path = os.path.join(root_dir, filename)
        if os.path.isfile(file_path):
            if filename == "directory_structure_final.txt":
                with open(file_path, 'r') as f:
                    data = json.load(f)
            elif filename == "shopping/recently_viewed_items.json":
                with open(file_path, 'r') as f:
                    shopping_data = json.load(f)
                    for item in shopping_data['structure']['checkout_saved_recently_viewed_products']:
                        date = item['string_map_data']['Date']['value']
                        if date:
                            date = datetime.strptime(date, '%Y-%m-%d')
                            if date.weekday() < 5:
                                data[date.strftime('%Y-%m-%d')] = data.get(date.strftime('%Y-%m-%d'), 0) + 1
                            else:
                                data[f"Week {date.strftime('%Y-%W')}"] = data.get(f"Week {date.strftime('%Y-%W')}", 0) + 1

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        for date, count in data.items():
            writer.writerow([date, count, "Daily" if date.count('-') == 2 else "Weekly"])

root_dir = "root_dir"
process_directory(root_dir)