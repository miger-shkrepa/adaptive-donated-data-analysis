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

    message_counts = {}

    # Walk through the directory structure
    for subdir, _, files in os.walk(root_dir):
        if "inbox" in subdir:
            for file in sorted(files):
                if file.startswith("message_") and file.endswith(".json"):
                    file_path = os.path.join(subdir, file)
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            for message in data.get("messages", []):
                                timestamp_ms = message.get("timestamp_ms")
                                if timestamp_ms is not None:
                                    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
                                    week_str = f"Week {dt.strftime('%Y-%U')}"
                                    if week_str not in message_counts:
                                        message_counts[week_str] = 0
                                    message_counts[week_str] += 1
                    except (json.JSONDecodeError, OSError) as e:
                        raise ValueError(f"Error: Failed to read or parse file {file_path}. {e}")

    return message_counts

# Function to save the results to a CSV file
def save_to_csv(message_counts):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Week', 'Messages Sent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for week, count in message_counts.items():
            writer.writerow({'Week': week, 'Messages Sent': count})

# Main function to execute the script
def main():
    try:
        message_counts = count_messages_per_week(root_dir)
        save_to_csv(message_counts)
        print("Results saved to query_responses/results.csv")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()