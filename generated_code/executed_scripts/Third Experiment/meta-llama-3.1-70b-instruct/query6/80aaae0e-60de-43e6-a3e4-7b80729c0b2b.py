import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    changes = []
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Check if the logged_information directory exists
        logged_info_dir = os.path.join(root_dir, "logged_information")
        if not os.path.exists(logged_info_dir):
            return changes

        # Check if the policy_updates_and_permissions directory exists
        policy_updates_dir = os.path.join(logged_info_dir, "policy_updates_and_permissions")
        if not os.path.exists(policy_updates_dir):
            return changes

        # Check if the notification_of_privacy_policy_updates.json file exists
        notification_file = os.path.join(policy_updates_dir, "notification_of_privacy_policy_updates.json")
        if not os.path.exists(notification_file):
            return changes

        # Read the notification_of_privacy_policy_updates.json file
        with open(notification_file, 'r') as file:
            # Since the exact structure of the json file is not provided, 
            # we assume it's a list of dictionaries with 'string_map_data' key
            import json
            data = json.load(file)
            for item in data:
                if 'string_map_data' in item:
                    string_map_data = item['string_map_data']
                    if 'Consent Status' in string_map_data:
                        consent_status = string_map_data['Consent Status']['value']
                        impression_time = string_map_data['Impression Time']['value']
                        changes.append({
                            'Changed': 'Consent Status',
                            'New Value': consent_status,
                            'Change Date': impression_time
                        })

        # Check if the profile_photos.json file exists
        profile_photos_file = os.path.join(root_dir, "profile_photos.json")
        if os.path.exists(profile_photos_file):
            # Read the profile_photos.json file
            with open(profile_photos_file, 'r') as file:
                # Since the exact structure of the json file is not provided, 
                # we assume it's a list of dictionaries with 'title' key
                import json
                data = json.load(file)
                for item in data:
                    if 'title' in item:
                        title = item['title']
                        creation_timestamp = item['creation_timestamp']
                        date = datetime.fromtimestamp(creation_timestamp).strftime('%Y-%m-%d')
                        changes.append({
                            'Changed': 'Profile Picture',
                            'New Value': title,
                            'Change Date': date
                        })

    except Exception as e:
        raise ValueError("Error: " + str(e))

    return changes

def save_to_csv(changes):
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Changed', 'New Value', 'Change Date'])
        writer.writeheader()
        for change in changes:
            writer.writerow(change)

def main():
    changes = get_account_changes(root_dir)
    if not changes:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Changed', 'New Value', 'Change Date'])
            writer.writeheader()
    else:
        save_to_csv(changes)

if __name__ == "__main__":
    main()