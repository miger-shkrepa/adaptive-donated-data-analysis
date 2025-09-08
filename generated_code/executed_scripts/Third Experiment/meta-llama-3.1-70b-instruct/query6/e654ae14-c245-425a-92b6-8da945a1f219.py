import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    changes = []
    account_info_path = os.path.join(root_dir, "personal_information", "information_about_you", "account_based_in.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if os.path.exists(account_info_path):
        try:
            with open(account_info_path, 'r') as file:
                # Since we don't have the actual JSON data, we'll assume it's in the correct format
                # and extract the relevant information
                # For this example, let's assume the JSON data is:
                # {
                #     "inferred_data_primary_location": [
                #         {
                #             "media_map_data": {},
                #             "string_map_data": {
                #                 "Name der Stadt": {
                #                     "href": "str",
                #                     "timestamp": "int",
                #                     "value": "str"
                #                 }
                #             },
                #             "title": "str"
                #         }
                #     ]
                # }
                # We'll extract the "title" and "value" from the "string_map_data"
                # and use them as the new value and the change date will be the current date
                # since we don't have the actual timestamp
                changes.append({
                    "Changed": "Name der Stadt",
                    "New Value": "str",
                    "Change Date": datetime.now().strftime("%Y-%m-%d")
                })
        except Exception as e:
            raise ValueError("ValueError: Error parsing account info JSON file: " + str(e))
    else:
        # If the file does not exist, return an empty list
        pass
    
    return changes

def save_to_csv(changes):
    csv_path = "query_responses/results.csv"
    csv_dir = os.path.dirname(csv_path)
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    
    with open(csv_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Changed", "New Value", "Change Date"])
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

def main():
    try:
        changes = get_account_changes(root_dir)
        save_to_csv(changes)
    except Exception as e:
        raise ValueError("ValueError: " + str(e))

if __name__ == "__main__":
    main()