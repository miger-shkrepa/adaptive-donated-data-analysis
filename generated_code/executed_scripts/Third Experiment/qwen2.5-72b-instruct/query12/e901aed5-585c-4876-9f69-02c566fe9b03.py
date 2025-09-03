import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize a dictionary to store the count of messages per week
    messages_per_week = {}

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if "messages" in data:
                        for message in data["messages"]:
                            if "timestamp_ms" in message:
                                timestamp_ms = message["timestamp_ms"]
                                timestamp = datetime.fromtimestamp(timestamp_ms / 1000)
                                week = timestamp.strftime("Week %Y-%W")
                                if week not in messages_per_week:
                                    messages_per_week[week] = 0
                                messages_per_week[week] += 1

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for week, count in messages_per_week.items():
            writer.writerow({'Week': week, 'Messages Sent': count})

except FileNotFoundError as e:
    print(e)
except json.JSONDecodeError as e:
    print(f"Error: JSON decoding error - {e}")
except Exception as e:
    print(f"Error: An unexpected error occurred - {e}")