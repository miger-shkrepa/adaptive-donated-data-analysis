import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"
account_info_file = os.path.join(root_dir, "accounts_center/accounts_center_info.json")
output_file = "query_responses/results.csv"

def parse_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def get_account_info(file_path):
    if not os.path.exists(file_path):
        return {}

    with open(file_path, 'r') as f:
        data = json.load(f)

    account_info = data['accounts_center_info']['account_data'][0]['string_map_data']
    return {
        'username': account_info['Username']['value'],
        'phone_number': account_info['Phone Number']['value'],
        'email': account_info['Email']['value'],
        'change_date': parse_date(account_info['Username']['timestamp'])
    }

def write_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Changed', 'New Value', 'Change Date'])
        for key, value in data.items():
            writer.writerow([key, value, data['change_date']])

try:
    account_info = get_account_info(account_info_file)
    write_to_csv(account_info, output_file)
except Exception as e:
    print(f"Error: {str(e)}")