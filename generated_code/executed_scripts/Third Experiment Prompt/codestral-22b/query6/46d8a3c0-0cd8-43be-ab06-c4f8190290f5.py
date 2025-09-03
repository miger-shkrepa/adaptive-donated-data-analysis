import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
output_file = "query_responses/results.csv"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def get_profile_info(profile_info):
    info = {}
    if profile_info:
        for item in profile_info:
            info['Username'] = item['string_map_data']['Username']['value']
            info['Email'] = item['string_map_data']['Email']['value']
            info['Phone Confirmed'] = item['string_map_data']['Phone Confirmed']['value']
            info['Date of birth'] = item['string_map_data']['Date of birth']['value']
            info['Gender'] = item['string_map_data']['Gender']['value']
    return info

def get_changes(old_info, new_info):
    changes = []
    for key in old_info:
        if old_info[key] != new_info[key]:
            changes.append({'Changed': key, 'New Value': new_info[key], 'Change Date': datetime.now().strftime('%Y-%m-%d')})
    return changes

def main():
    personal_info_dir = os.path.join(root_dir, 'personal_information', 'personal_information')
    if not os.path.exists(personal_info_dir):
        raise FileNotFoundError("FileNotFoundError: The personal information directory does not exist.")

    profile_info_file = os.path.join(personal_info_dir, 'instagram_profile_information.json')
    profile_info = load_json(profile_info_file)
    if profile_info is None:
        raise FileNotFoundError("FileNotFoundError: The Instagram profile information file does not exist.")

    if 'structure' in profile_info:
        profile_info = profile_info['structure']['profile_account_insights']
        old_info = get_profile_info(profile_info)
    else:
        old_info = {}

    changes = []
    for file in sorted(os.listdir(personal_info_dir)):
        if file.startswith('instagram_profile_information_') and file.endswith('.json'):
            profile_info = load_json(os.path.join(personal_info_dir, file))
            if profile_info is not None and 'structure' in profile_info:
                profile_info = profile_info['structure']['profile_account_insights']
                new_info = get_profile_info(profile_info)
                changes.extend(get_changes(old_info, new_info))
                old_info = new_info

    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Changed', 'New Value', 'Change Date'])
        writer.writeheader()
        writer.writerows(changes)

if __name__ == "__main__":
    main()