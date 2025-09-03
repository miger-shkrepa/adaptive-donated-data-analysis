import os
import csv
import json
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Function to check if the directory exists
def check_directory_exists(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"FileNotFoundError: The root directory does not exist.")

# Function to parse the timestamp and return the week in 'Week YYYY-WW' format
def get_week_from_timestamp(timestamp_ms):
    timestamp_s = int(timestamp_ms) / 1000
    dt = datetime.fromtimestamp(timestamp_s)
    return f"Week {dt.strftime('%Y-%U')}"

# Function to count messages per week
def count_messages_per_week(root_dir):
    check_directory_exists(root_dir)
    
    # Dictionary to store the count of messages per week
    messages_per_week = {}

    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith("message_") and filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        for message in data.get('messages', []):
                            if 'timestamp_ms' in message:
                                week = get_week_from_timestamp(message['timestamp_ms'])
                                if week in messages_per_week:
                                    messages_per_week[week] += 1
                                else:
                                    messages_per_week[week] = 1
                except (FileNotFoundError, ValueError) as e:
                    print(f"Error processing file {file_path}: {e}")
                    continue

    return messages_per_week

# Function to write the results to a CSV file
def write_results_to_csv(messages_per_week, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Week', 'Messages Sent'])
            for week, count in sorted(messages_per_week.items()):
                writer.writerow([week, count])
    except IOError as e:
        raise IOError(f"IOError: Failed to write to the output file. {e}")

# Main function to execute the script
def main():
    try:
        messages_per_week = count_messages_per_week(root_dir)
        write_results_to_csv(messages_per_week, 'query_responses/results.csv')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()