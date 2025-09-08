import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse message files and count messages per week
def count_messages_per_week(root_dir):
    message_counts = {}

    # Walk through the directory structure
    for subdir, _, files in os.walk(root_dir):
        if 'inbox' in subdir:
            for file in sorted(files):
                if file.startswith('message_') and file.endswith('.json'):
                    file_path = os.path.join(subdir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            messages = data.get('messages', [])
                            for message in messages:
                                timestamp_ms = message.get('timestamp_ms')
                                if timestamp_ms:
                                    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
                                    week_str = f"Week {dt.isocalendar()[0]}-{dt.isocalendar()[1]:02}"
                                    if week_str in message_counts:
                                        message_counts[week_str] += 1
                                    else:
                                        message_counts[week_str] = 1
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        print(f"Error: {e}")
                        continue

    return message_counts

# Function to write the results to a CSV file
def write_to_csv(message_counts):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for week, count in sorted(message_counts.items()):
            writer.writerow({'Week': week, 'Messages Sent': count})

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    message_counts = count_messages_per_week(root_dir)
    write_to_csv(message_counts)

if __name__ == "__main__":
    main()