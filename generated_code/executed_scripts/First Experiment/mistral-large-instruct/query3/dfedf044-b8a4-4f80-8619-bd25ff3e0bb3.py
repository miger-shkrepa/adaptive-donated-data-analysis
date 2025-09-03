import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to parse JSON files and extract relevant data
def parse_json_files(directory):
    data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        json_data = json.load(f)
                        data.append(json_data)
                except FileNotFoundError:
                    raise FileNotFoundError("FileNotFoundError: The file does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("ValueError: The file is not a valid JSON.")
    return data

# Function to process data and generate the required CSV
def process_data(data):
    daily_counts = {}
    weekly_counts = {}

    for item in data:
        if "creation_timestamp" in item:
            timestamp = item["creation_timestamp"]
            date = datetime.fromtimestamp(timestamp).date()
            week = date.strftime("Week %Y-%W")

            if date not in daily_counts:
                daily_counts[date] = 0
            daily_counts[date] += 1

            if week not in weekly_counts:
                weekly_counts[week] = 0
            weekly_counts[week] += 1

    return daily_counts, weekly_counts

# Function to write the results to a CSV file
def write_to_csv(daily_counts, weekly_counts):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    data = parse_json_files(root_dir)
    daily_counts, weekly_counts = process_data(data)
    write_to_csv(daily_counts, weekly_counts)

if __name__ == "__main__":
    main()