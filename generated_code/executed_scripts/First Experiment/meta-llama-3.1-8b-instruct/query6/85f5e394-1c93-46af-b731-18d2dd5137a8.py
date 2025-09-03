import os
import csv
import json
from datetime import datetime

def get_instagram_account_changes(root_dir):
    try:
        # Walk through the directory and find all JSON files
        json_files = []
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))

        # Initialize a dictionary to store the changes
        changes = {}

        # Iterate over the JSON files
        for file in json_files:
            with open(file, 'r') as f:
                data = json.load(f)
                # Check if the file contains Instagram profile information
                if 'instagram_profile_information.json' in file:
                    # Extract the profile information
                    profile_info = data['profile_account_insights'][0]['string_map_data']
                    # Iterate over the profile information
                    for key, value in profile_info.items():
                        # Check if the key is a change (e.g., name, phone, email)
                        if key in ['First Name', 'Last Name', 'Phone Number', 'Email Address']:
                            # Get the current date
                            current_date = datetime.now().strftime('%Y-%m-%d')
                            # Check if the key is already in the changes dictionary
                            if key in changes:
                                # If the key is already in the dictionary, append the new value and date
                                changes[key].append((current_date, value['value']))
                            else:
                                # If the key is not in the dictionary, add it with the new value and date
                                changes[key] = [(current_date, value['value'])]

        # Create a list to store the changes in the required format
        change_list = []
        # Iterate over the changes dictionary
        for key, value in changes.items():
            # Iterate over the values in the dictionary
            for date, new_value in value:
                # Append the change to the list
                change_list.append([key, new_value, date])

        # Write the changes to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            # Write the header
            writer.writerow(['Changed', 'New Value', 'Change Date'])
            # Write the changes
            writer.writerows(change_list)

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError("ValueError: The JSON file is not valid.")
    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the JSON file.")

# Declare the variable referring to the file input
root_dir = "root_dir"

# Call the function
get_instagram_account_changes(root_dir)