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

        # Initialize a list to store the changes
        changes = []

        # Iterate over the files in the personal_information directory
        personal_info_dir = os.path.join(root_dir, "personal_information")
        if os.path.exists(personal_info_dir):
            for filename in os.listdir(personal_info_dir):
                if filename == "instagram_profile_information.json":
                    file_path = os.path.join(personal_info_dir, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for item in data["profile_account_insights"]:
                            for key, value in item["string_map_data"].items():
                                if key in ["Contact Syncing", "First Close Friends Story Time", "First Country Code", "First Story Time", "Has Shared Live Video", "Last Login", "Last Logout", "Last Story Time"]:
                                    changes.append({
                                        "Changed": key,
                                        "New Value": value["value"],
                                        "Change Date": datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")
                                    })

        # Write the changes to a CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
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