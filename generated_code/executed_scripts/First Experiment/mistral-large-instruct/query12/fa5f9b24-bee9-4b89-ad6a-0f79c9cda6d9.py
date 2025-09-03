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

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "inbox" in dirpath:
            for filename in filenames:
                if filename.startswith("message_") and filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            messages = data.get("messages", [])
                            for message in messages:
                                timestamp_ms = message.get("timestamp_ms")
                                if timestamp_ms:
                                    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
                                    week_str = f"Week {dt.strftime('%Y-%W')}"
                                    if week_str not in messages_per_week:
                                        messages_per_week[week_str] = 0
                                    messages_per_week[week_str] += 1
                    except json.JSONDecodeError:
                        raise ValueError(f"Error: Invalid JSON format in file {file_path}.")
                    except Exception as e:
                        raise ValueError(f"Error: {str(e)}")

    return messages_per_week

# Function to save results to a CSV file
def save_to_csv(messages_per_week, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for week, count in messages_per_week.items():
                writer.writerow({'Week': week, 'Messages Sent': count})
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

# Main function to execute the script
def main():
    try:
        messages_per_week = count_messages_per_week(root_dir)
        save_to_csv(messages_per_week, 'query_responses/results.csv')
        print("CSV file generated successfully.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()