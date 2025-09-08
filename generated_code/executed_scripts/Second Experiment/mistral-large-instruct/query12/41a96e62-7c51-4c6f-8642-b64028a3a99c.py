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
    message_counts = {}

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "inbox" in dirpath:
            for filename in filenames:
                if filename.startswith("message_") and filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            messages = data.get("messages", [])
                            for message in messages:
                                timestamp_ms = message.get("timestamp_ms")
                                if timestamp_ms:
                                    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
                                    week_str = f"Week {dt.strftime('%Y-%U')}"
                                    if week_str in message_counts:
                                        message_counts[week_str] += 1
                                    else:
                                        message_counts[week_str] = 1
                    except FileNotFoundError:
                        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
                    except json.JSONDecodeError:
                        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

    return message_counts

# Function to write the results to a CSV file
def write_to_csv(message_counts, output_csv):
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for week, count in message_counts.items():
                writer.writerow({'Week': week, 'Messages Sent': count})
    except Exception as e:
        raise IOError(f"Error: IOError: Failed to write to the CSV file. {str(e)}")

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    message_counts = count_messages_per_week(root_dir)

    if not os.path.exists(os.path.dirname(output_csv)):
        os.makedirs(os.path.dirname(output_csv))

    write_to_csv(message_counts, output_csv)

if __name__ == "__main__":
    main()