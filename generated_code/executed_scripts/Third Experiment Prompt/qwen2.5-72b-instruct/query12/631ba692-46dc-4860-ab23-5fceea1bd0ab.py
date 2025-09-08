import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to process messages and count per week
def count_messages_per_week(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store message counts per week
        message_counts = {}

        # Path to the inbox directory
        inbox_dir = os.path.join(root_dir, "your_instagram_activity", "messages", "inbox")

        if not os.path.exists(inbox_dir):
            return message_counts

        # Iterate over each conversation directory in the inbox
        for conversation_dir in os.listdir(inbox_dir):
            conversation_path = os.path.join(inbox_dir, conversation_dir)
            if os.path.isdir(conversation_path):
                message_files = sorted([f for f in os.listdir(conversation_path) if f.startswith("message_") and f.endswith(".json")])

                for message_file in message_files:
                    message_path = os.path.join(conversation_path, message_file)
                    with open(message_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        messages = data.get("messages", [])
                        for message in messages:
                            timestamp_ms = message.get("timestamp_ms")
                            if timestamp_ms:
                                timestamp = datetime.fromtimestamp(int(timestamp_ms) / 1000)
                                week = timestamp.strftime('%Y-%W')
                                if week not in message_counts:
                                    message_counts[week] = 0
                                message_counts[week] += 1

        return message_counts

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Function to write the results to a CSV file
def write_to_csv(message_counts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for week, count in sorted(message_counts.items(), key=lambda x: datetime.strptime(x[0] + '-1', '%Y-%W-%w')):
                writer.writerow({'Week': f"Week {week}", 'Messages Sent': count})
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

# Main function to execute the script
def main():
    try:
        message_counts = count_messages_per_week(root_dir)
        write_to_csv(message_counts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()