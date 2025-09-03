import csv
import json
import os

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Set the input file path
input_file = os.path.join(root_dir, 'personal_information', 'profile_changes.json')

# Check if the input file exists
if not os.path.exists(input_file):
    print("Warning: Input file does not exist. Returning CSV with only column headers.")
else:
    try:
        # Load the JSON data
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Extract the required data
        changes = []
        for profile_change in data['profile_profile_change']:
            changed = profile_change['string_map_data']['Changed']['value']
            new_value = profile_change['string_map_data']['New Value']['value']
            change_date = profile_change['string_map_data']['Change Date']['timestamp']
            changes.append([changed, new_value, change_date])

        # Write the data to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Changed', 'New Value', 'Change Date'])  # header
            writer.writerows(changes)

        print("Query results written to query_responses/results.csv")

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON data: " + str(e))
    except KeyError as e:
        raise ValueError("Error: Missing key in JSON data: " + str(e))
    except Exception as e:
        raise ValueError("Error: Unexpected error: " + str(e))