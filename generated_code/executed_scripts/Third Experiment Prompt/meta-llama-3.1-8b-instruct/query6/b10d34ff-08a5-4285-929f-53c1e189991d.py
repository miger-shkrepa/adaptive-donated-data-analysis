import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as file:
                        data = json.load(file)
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON file {filepath}: {e}")
                    continue

                # Check if the file contains user information
                if 'personal_information' in data and 'personal_information' in data['personal_information']:
                    user_info = data['personal_information']['personal_information']
                    for info in user_info:
                        if 'profile_user' in info:
                            user_data = info['profile_user']
                            for key, value in user_data.items():
                                if key == 'string_map_data':
                                    for k, v in value.items():
                                        if k in ['Name', 'Phone Number', 'Email']:
                                            writer.writerow([k, v['value'], '2022-01-01'])

                # Check if the file contains login and profile creation information
                if 'security_and_login_information' in data and 'login_and_profile_creation' in data['security_and_login_information']:
                    login_info = data['security_and_login_information']['login_and_profile_creation']
                    for info in login_info:
                        if 'instagram_signup_details' in info:
                            signup_data = info['instagram_signup_details']
                            for key, value in signup_data.items():
                                if key == 'account_history_registration_info':
                                    for reg_info in value:
                                        if 'string_map_data' in reg_info:
                                            for k, v in reg_info['string_map_data'].items():
                                                if k in ['Username', 'Phone Number', 'Email']:
                                                    writer.writerow([k, v['value'], '2022-01-01'])

                # Check if the file contains profile information
                if 'personal_information' in data and 'information_about_you' in data['personal_information']:
                    profile_info = data['personal_information']['information_about_you']
                    for info in profile_info:
                        if 'profile_based_in' in info:
                            based_in_data = info['profile_based_in']
                            for key, value in based_in_data.items():
                                if key == 'inferred_data_primary_location':
                                    for loc in value:
                                        if 'string_map_data' in loc:
                                            for k, v in loc['string_map_data'].items():
                                                if k in ['City Name']:
                                                    writer.writerow([k, v['value'], '2022-01-01'])

                # Check if the file contains device information
                if 'personal_information' in data and 'device_information' in data['personal_information']:
                    device_info = data['personal_information']['device_information']
                    for info in device_info:
                        if 'camera_information' in info:
                            camera_data = info['camera_information']
                            for key, value in camera_data.items():
                                if key == 'devices_camera':
                                    for cam in value:
                                        if 'string_map_data' in cam:
                                            for k, v in cam['string_map_data'].items():
                                                if k in ['Device ID', 'Supported SDK Versions']:
                                                    writer.writerow([k, v['value'], '2022-01-01'])

                # Check if the file contains location information
                if 'personal_information' in data and 'information_about_you' in data['personal_information']:
                    location_info = data['personal_information']['information_about_you']
                    for info in location_info:
                        if 'locations_of_interest' in info:
                            locations_data = info['locations_of_interest']
                            for key, value in locations_data.items():
                                if key == 'label_values':
                                    for loc in value:
                                        if 'vec' in loc:
                                            for v in loc['vec']:
                                                if 'value' in v:
                                                    writer.writerow(['Location', v['value'], '2022-01-01'])