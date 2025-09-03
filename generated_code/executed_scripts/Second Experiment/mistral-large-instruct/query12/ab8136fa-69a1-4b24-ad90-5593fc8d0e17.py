import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = "query_responses/results.csv"

# Function to parse message files and count messages per week
def count_messages_per_week(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    messages_per_week = {}

    # Traverse the directory structure
    for subdir, _, files in os.walk(os.path.join(root_dir, "messages", "inbox")):
        for file in files:
            if file.startswith("message_") and file.endswith(".json"):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for message in data.get("messages", []):
                            timestamp_ms = message.get("timestamp_ms")
                            if timestamp_ms:
                                dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
                                week_str = f"Week {dt.strftime('%Y-%W')}"
                                if week_str not in messages_per_week:
                                    messages_per_week[week_str] = 0
                                messages_per_week[week_str] += 1
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Error processing file {file_path}: {e}")

    return messages_per_week

# Function to write the results to a CSV file
def write_to_csv(messages_per_week, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for week, count in messages_per_week.items():
                writer.writerow({'Week': week, 'Messages Sent': count})
    except IOError as e:
        raise IOError(f"Error: Unable to write to CSV file. {e}")

# Main function to execute the script
def main():
    try:
        messages_per_week = count_messages_per_week(root_dir)
        write_to_csv(messages_per_week, output_csv)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()