import os
import csv
from datetime import datetime

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    changes = []
    personal_info_path = os.path.join(root_dir, "personal_information")
    if os.path.exists(personal_info_path):
        personal_info_json_path = os.path.join(personal_info_path, "personal_information.json")
        if os.path.exists(personal_info_json_path):
            with open(personal_info_json_path, 'r') as file:
                personal_info_data = eval(file.read())
                for profile in personal_info_data["profile_user"]:
                    string_map_data = profile["string_map_data"]
                    for key, value in string_map_data.items():
                        if key in ["Bio", "Date of birth"]:
                            changes.append({
                                "Changed": key,
                                "New Value": value["value"],
                                "Change Date": datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")
                            })

        signup_details_json_path = os.path.join(personal_info_path, "signup_details.json")
        if os.path.exists(signup_details_json_path):
            with open(signup_details_json_path, 'r') as file:
                signup_details_data = eval(file.read())
                for registration in signup_details_data["account_history_registration_info"]:
                    string_map_data = registration["string_map_data"]
                    for key, value in string_map_data.items():
                        if key in ["Email", "Phone Number"]:
                            changes.append({
                                "Changed": key,
                                "New Value": value["value"],
                                "Change Date": datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")
                            })

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ["Changed", "New Value", "Change Date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

except Exception as e:
    raise ValueError("Error: " + str(e))