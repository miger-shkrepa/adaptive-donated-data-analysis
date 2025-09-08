import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse JSON files and extract relevant data
def parse_json_files(directory):
    data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        json_data = json.load(f)
                        data.append(json_data)
                except FileNotFoundError:
                    raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
                except json.JSONDecodeError:
                    raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")
    return data

# Function to process the data and generate the CSV file
def process_data(data):
    daily_counts = {}
    weekly_counts = {}

    for item in data:
        if 'creation_timestamp' in item:
            timestamp = item['creation_timestamp']
            date = datetime.fromtimestamp(timestamp)
            date_str = date.strftime('%Y-%m-%d')
            week_str = f"Week {date.strftime('%Y-%W')}"

            if date_str in daily_counts:
                daily_counts[date_str] += 1
            else:
                daily_counts[date_str] = 1

            if week_str in weekly_counts:
                weekly_counts[week_str] += 1
            else:
                weekly_counts[week_str] = 1

    return daily_counts, weekly_counts

# Function to write the results to a CSV file
def write_csv(daily_counts, weekly_counts):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    data = parse_json_files(root_dir)
    daily_counts, weekly_counts = process_data(data)
    write_csv(daily_counts, weekly_counts)

if __name__ == "__main__":
    main()