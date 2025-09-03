import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize a dictionary to count messages per week
    messages_per_week = {}

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(os.path.join(root_dir, "inbox")):
        for filename in filenames:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for message in data.get("messages", []):
                        timestamp = message.get("timestamp_ms")
                        if timestamp:
                            date = datetime.fromtimestamp(timestamp / 1000)
                            week = date.strftime("Week %Y-%W")
                            messages_per_week[week] = messages_per_week.get(week, 0) + 1

    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for week, count in messages_per_week.items():
            writer.writerow({'Week': week, 'Messages Sent': count})

except FileNotFoundError as e:
    print(e)
except json.JSONDecodeError as e:
    raise ValueError(f"Error: JSON decoding error - {e}")
except Exception as e:
    raise ValueError(f"Error: An unexpected error occurred - {e}")