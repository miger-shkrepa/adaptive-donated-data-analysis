import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        signup_details_path = os.path.join(root_dir, "signup_details.json")
        if not os.path.exists(signup_details_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Changed', 'New Value', 'Change Date'])
            return

        with open(signup_details_path, 'r') as file:
            signup_details = json.load(file)

        changes = []
        for entry in signup_details["account_history_registration_info"]:
            string_map_data = entry["string_map_data"]
            for key, value in string_map_data.items():
                if key in ["Device", "Email", "IP Address", "Phone Number", "Username"]:
                    timestamp = datetime.fromtimestamp(value["timestamp"] / 1000).strftime('%Y-%m-%d')
                    changes.append([key, value["value"], timestamp])

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Changed', 'New Value', 'Change Date'])
            writer.writerows(changes)

    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

get_account_changes()