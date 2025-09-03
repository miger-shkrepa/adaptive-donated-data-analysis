import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize dictionary to store messages sent per week
        messages_sent_per_week = {}

        # Iterate over subfolders in 'your_instagram_activity' directory
        your_instagram_activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(your_instagram_activity_dir):
            for subfolder in os.listdir(your_instagram_activity_dir):
                subfolder_path = os.path.join(your_instagram_activity_dir, subfolder)
                if os.path.isdir(subfolder_path):
                    # Iterate over files in subfolder
                    for filename in os.listdir(subfolder_path):
                        if filename.startswith('message_') and filename.endswith('.json'):
                            file_path = os.path.join(subfolder_path, filename)
                            with open(file_path, 'r') as file:
                                data = json.load(file)
                                # Assuming 'timestamp' is in seconds since epoch
                                timestamp = data['string_list_data'][0]['timestamp']
                                week = datetime.utcfromtimestamp(timestamp).strftime('Week %Y-%U')
                                if week not in messages_sent_per_week:
                                    messages_sent_per_week[week] = 1
                                else:
                                    messages_sent_per_week[week] += 1

        # Write results to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Week', 'Messages Sent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for week, messages_sent in messages_sent_per_week.items():
                writer.writerow({'Week': week, 'Messages Sent': messages_sent})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON file: {e}")

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred: {e}")

get_messages_sent_per_week(root_dir)