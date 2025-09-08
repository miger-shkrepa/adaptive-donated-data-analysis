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
                    raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
                except json.JSONDecodeError:
                    raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")
    return data

# Function to process the data and generate the CSV file
def generate_csv(data):
    csv_data = []
    for item in data:
        if "creation_timestamp" in item:
            timestamp = item["creation_timestamp"]
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            week = datetime.fromtimestamp(timestamp).strftime('Week %Y-%W')
            csv_data.append([date, 1, 'Daily'])
            csv_data.append([week, 1, 'Weekly'])

    # Write the data to a CSV file
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in csv_data:
                writer.writerow(dict(zip(fieldnames, row)))
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    data = parse_json_files(root_dir)
    generate_csv(data)

if __name__ == "__main__":
    main()