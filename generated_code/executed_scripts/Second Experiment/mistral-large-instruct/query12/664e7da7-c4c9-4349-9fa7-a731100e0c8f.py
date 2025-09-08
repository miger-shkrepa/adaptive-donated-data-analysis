import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to parse message files and count messages per week
def count_messages_per_week(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    messages_per_week = {}

    # Traverse the directory structure
    for subdir, _, files in os.walk(os.path.join(root_dir, 'messages', 'inbox')):
        for file in sorted(files):
            if file.startswith('message_') and file.endswith('.json'):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for message in data.get('messages', []):
                            timestamp_ms = message.get('timestamp_ms')
                            if timestamp_ms:
                                dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
                                week_str = f"Week {dt.strftime('%Y-%W')}"
                                if week_str in messages_per_week:
                                    messages_per_week[week_str] += 1
                                else:
                                    messages_per_week[week_str] = 1
                except (json.JSONDecodeError, OSError) as e:
                    print(f"Error reading file {file_path}: {e}")

    return messages_per_week

# Function to write the results to a CSV file
def write_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
            for week, count in sorted(data.items()):
                writer.writerow([week, count])
    except OSError as e:
        raise OSError(f"Error: Unable to write to CSV file. {e}")

# Main function to execute the script
def main():
    try:
        messages_per_week = count_messages_per_week(root_dir)
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        write_to_csv(messages_per_week, output_path)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()