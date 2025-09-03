import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Iterate through 'security_and_login_information' directory
        security_dir = os.path.join(root_dir, 'security_and_login_information')
        if os.path.exists(security_dir):
            login_activity_file = os.path.join(security_dir, 'login_activity.json')
            if os.path.exists(login_activity_file):
                with open(login_activity_file, 'r') as f:
                    login_activity_data = json.load(f)
                    if 'account_history_login_history' in login_activity_data:
                        for activity in login_activity_data['account_history_login_history']:
                            if 'string_map_data' in activity and 'User Agent' in activity['string_map_data']:
                                companies.add(activity['string_map_data']['User Agent']['value'])

        # Iterate through 'personal_information' directory
        personal_dir = os.path.join(root_dir, 'personal_information')
        if os.path.exists(personal_dir):
            device_info_file = os.path.join(personal_dir, 'device_information', 'devices.json')
            if os.path.exists(device_info_file):
                with open(device_info_file, 'r') as f:
                    device_info_data = json.load(f)
                    if 'devices_devices' in device_info_data:
                        for device in device_info_data['devices_devices']:
                            if 'string_map_data' in device and 'User Agent' in device['string_map_data']:
                                companies.add(device['string_map_data']['User Agent']['value'])

        # Iterate through 'your_instagram_activity' directory
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(activity_dir):
            messages_dir = os.path.join(activity_dir, 'messages')
            if os.path.exists(messages_dir):
                for message_file in os.listdir(messages_dir):
                    if message_file.endswith('.json'):
                        message_file_path = os.path.join(messages_dir, message_file)
                        with open(message_file_path, 'r') as f:
                            message_data = json.load(f)
                            if 'messages' in message_data:
                                for message in message_data['messages']:
                                    if 'sender_name' in message:
                                        companies.add(message['sender_name'])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

    return companies

def write_to_csv(companies):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Company Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company in companies:
            writer.writerow({'Company Name': company})

companies = get_companies_with_access(root_dir)
write_to_csv(companies)