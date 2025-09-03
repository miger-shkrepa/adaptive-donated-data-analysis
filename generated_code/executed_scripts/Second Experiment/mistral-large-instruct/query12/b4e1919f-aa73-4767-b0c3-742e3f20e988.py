import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse message files and count messages per week
def count_messages_per_week(root_dir):
    messages_per_week = {}

    # Walk through the directory structure
    for subdir, _, files in os.walk(root_dir):
        if 'inbox' in subdir:
            for file in sorted(files):
                if file.startswith('message_') and file.endswith('.json'):
                    file_path = os.path.join(subdir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            for message in data.get('messages', []):
                                timestamp_ms = message.get('timestamp_ms')
                                if timestamp_ms:
                                    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
                                    week_str = f"Week {dt.strftime('%Y-%U')}"
                                    if week_str not in messages_per_week:
                                        messages_per_week[week_str] = 0
                                    messages_per_week[week_str] += 1
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        print(f"Error: {e}")
                        continue

    return messages_per_week

# Function to write the results to a CSV file
def write_to_csv(messages_per_week):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for week, count in sorted(messages_per_week.items()):
            writer.writerow({'Week': week, 'Messages Sent': count})

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    messages_per_week = count_messages_per_week(root_dir)
    write_to_csv(messages_per_week)

if __name__ == "__main__":
    main()