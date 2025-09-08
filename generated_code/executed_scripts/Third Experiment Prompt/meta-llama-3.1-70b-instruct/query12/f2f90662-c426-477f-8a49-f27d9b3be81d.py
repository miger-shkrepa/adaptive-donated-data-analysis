import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_weekly_messages(root_dir):
    weekly_messages = {}
    for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, 'media', 'posts')):
        for filename in filenames:
            if filename.startswith('message_') and filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as file:
                        data = json.load(file)
                        timestamp = data['creation_timestamp']
                        week = datetime.fromtimestamp(timestamp).strftime('%Y-%W')
                        if week in weekly_messages:
                            weekly_messages[week] += 1
                        else:
                            weekly_messages[week] = 1
                except FileNotFoundError:
                    raise FileNotFoundError("FileNotFoundError: The file {} does not exist.".format(filepath))
                except json.JSONDecodeError:
                    raise ValueError("ValueError: The file {} is not a valid JSON file.".format(filepath))
    return weekly_messages

def save_to_csv(weekly_messages):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Week', 'Messages Sent'])
        for week, messages in weekly_messages.items():
            writer.writerow([week, messages])

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    weekly_messages = get_weekly_messages(root_dir)
    save_to_csv(weekly_messages)

if __name__ == "__main__":
    main()