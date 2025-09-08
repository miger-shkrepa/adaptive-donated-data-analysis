import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_instagram_account_changes(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize lists to store changes
        changes = []

        # Iterate over the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "personal_information.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for profile in data["profile_user"]:
                            string_map_data = profile.get("string_map_data", {})
                            for key, value in string_map_data.items():
                                if key in ["Bio", "Date of birth"]:
                                    changes.append({
                                        "Changed": key,
                                        "New Value": value["value"],
                                        "Change Date": datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")
                                    })

        # Save changes to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ["Changed", "New Value", "Change Date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in changes:
                writer.writerow(change)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON - {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

get_instagram_account_changes(root_dir)