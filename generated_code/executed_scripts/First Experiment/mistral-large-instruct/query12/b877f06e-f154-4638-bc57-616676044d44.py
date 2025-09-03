import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_week_from_timestamp(timestamp_ms):
    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
    return f"Week {dt.strftime('%Y-%W')}"

def count_messages_per_week(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    messages_per_week = {}

    for subdir, _, files in os.walk(root_dir):
        if "inbox" in subdir:
            for file in sorted(files):
                if file.startswith("message_") and file.endswith(".json"):
                    file_path = os.path.join(subdir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            messages = data.get("messages", [])
                            for message in messages:
                                timestamp_ms = message.get("timestamp_ms")
                                if timestamp_ms is not None:
                                    week = get_week_from_timestamp(timestamp_ms)
                                    if week in messages_per_week:
                                        messages_per_week[week] += 1
                                    else:
                                        messages_per_week[week] = 1
                    except (json.JSONDecodeError, ValueError) as e:
                        raise ValueError(f"Error: Failed to parse JSON file {file_path}. {e}")

    return messages_per_week

def save_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
            for week, count in sorted(data.items()):
                writer.writerow([week, count])
    except IOError as e:
        raise IOError(f"Error: Failed to write to CSV file {output_path}. {e}")

if __name__ == "__main__":
    try:
        messages_per_week = count_messages_per_week(root_dir)
        save_to_csv(messages_per_week, 'query_responses/results.csv')
        print("CSV file generated successfully.")
    except Exception as e:
        print(e)