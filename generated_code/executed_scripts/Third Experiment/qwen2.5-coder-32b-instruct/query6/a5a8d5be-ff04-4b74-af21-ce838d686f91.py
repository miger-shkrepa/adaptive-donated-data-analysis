import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    changes = []

    try:
        signup_details_path = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation", "instagram_signup_details.json")
        if not os.path.exists(signup_details_path):
            raise FileNotFoundError("FileNotFoundError: The instagram_signup_details.json file does not exist.")

        with open(signup_details_path, 'r') as file:
            import json
            data = json.load(file)

            for entry in data.get("account_history_registration_info", []):
                string_map_data = entry.get("string_map_data", {})
                for key, value in string_map_data.items():
                    if key in ["Name", "Phone Number", "Email"]:
                        changes.append({
                            "Changed": key,
                            "New Value": value.get("value", ""),
                            "Change Date": datetime.fromtimestamp(value.get("timestamp", 0)).strftime('%Y-%m-%d')
                        })

    except FileNotFoundError as e:
        print(e)
        return []

    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
        return []

    return changes

def save_changes_to_csv(changes):
    try:
        os.makedirs(os.path.dirname('query_responses/results.csv'), exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Changed", "New Value", "Change Date"])
            writer.writeheader()
            writer.writerows(changes)

    except Exception as e:
        print(f"Error: Failed to write to CSV - {str(e)}")

if __name__ == "__main__":
    changes = get_account_changes(root_dir)
    save_changes_to_csv(changes)