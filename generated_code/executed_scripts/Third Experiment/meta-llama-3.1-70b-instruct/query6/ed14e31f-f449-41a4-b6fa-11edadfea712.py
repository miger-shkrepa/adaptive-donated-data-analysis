import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    changes = []
    try:
        account_history_dir = os.path.join(root_dir, "security_and_login_information", "login_and_profile_creation")
        if not os.path.exists(account_history_dir):
            raise FileNotFoundError("FileNotFoundError: The account history directory does not exist.")
        
        instagram_signup_details_file = os.path.join(account_history_dir, "instagram_signup_details.json")
        if not os.path.exists(instagram_signup_details_file):
            raise FileNotFoundError("FileNotFoundError: The instagram signup details file does not exist.")
        
        with open(instagram_signup_details_file, 'r') as file:
            import json
            data = json.load(file)
            for account_history in data["account_history_registration_info"]:
                string_map_data = account_history.get("string_map_data", {})
                for key, value in string_map_data.items():
                    if key in ["Name", "Phone Number", "Email"]:
                        changes.append({
                            "Changed": key,
                            "New Value": value["value"],
                            "Change Date": datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")
                        })
        
        account_info_dir = os.path.join(root_dir, "account_info")
        if os.path.exists(account_info_dir):
            account_info_file = os.path.join(account_info_dir, "account_info.json")
            if os.path.exists(account_info_file):
                with open(account_info_file, 'r') as file:
                    import json
                    data = json.load(file)
                    for account_info in data["account_info"]:
                        string_map_data = account_info.get("string_map_data", {})
                        for key, value in string_map_data.items():
                            if key in ["Name", "Phone Number", "Email"]:
                                changes.append({
                                    "Changed": key,
                                    "New Value": value["value"],
                                    "Change Date": datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")
                                })
        
        return changes
    
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(changes, filename):
    with open(filename, 'w', newline='') as file:
        fieldnames = ["Changed", "New Value", "Change Date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

def main():
    try:
        changes = get_account_changes(root_dir)
        save_to_csv(changes, 'query_responses/results.csv')
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            fieldnames = ["Changed", "New Value", "Change Date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    main()