import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_account_changes(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize lists to store changes
        changes = []

        # Check if 'string_map_data' file exists
        string_map_data_path = os.path.join(root_dir, 'string_map_data.json')
        if os.path.exists(string_map_data_path):
            # Parse 'string_map_data' file
            with open(string_map_data_path, 'r') as f:
                import json
                data = json.load(f)
                for key, value in data.items():
                    if key in ['Importzeit', 'Kontaktinformationen', 'Nachname', 'Vorname']:
                        changes.append({
                            'Changed': key,
                            'New Value': value['value'],
                            'Change Date': datetime.fromtimestamp(value['timestamp']).strftime('%Y-%m-%d')
                        })

        # Check if 'followers_and_following' directory exists
        followers_and_following_path = os.path.join(root_dir, 'followers_and_following')
        if os.path.exists(followers_and_following_path):
            # Parse 'followers_and_following' directory
            for filename in os.listdir(followers_and_following_path):
                file_path = os.path.join(followers_and_following_path, filename)
                if filename.endswith('.json'):
                    with open(file_path, 'r') as f:
                        import json
                        data = json.load(f)
                        for item in data.get('relationships_close_friends', []) + data.get('relationships_following', []) + data.get('relationships_follow_requests_received', []) + data.get('relationships_follow_requests_sent', []) + data.get('relationships_unfollowed_users', []) + data.get('relationships_permanent_follow_requests', []) + data.get('relationships_dismissed_suggested_users', []):
                            for string_data in item.get('string_list_data', []):
                                changes.append({
                                    'Changed': 'Followers and Following',
                                    'New Value': string_data['value'],
                                    'Change Date': datetime.fromtimestamp(string_data['timestamp']).strftime('%Y-%m-%d')
                                })

        # Save changes to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for change in changes:
                writer.writerow(change)

    except Exception as e:
        raise ValueError("Error: " + str(e))

get_account_changes(root_dir)