import os
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the target JSON file
profile_info_path = os.path.join(root_dir, "personal_information", "personal_information", "instagram_profile_information.json")

# Initialize the list to store the changes
changes = []

# Function to parse the timestamp and convert it to YYYY-MM-DD format
def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except (ValueError, OSError):
        return None

# Check if the file exists
if not os.path.exists(profile_info_path):
    # If the file does not exist, create an empty CSV with headers
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Changed', 'New Value', 'Change Date'])
    raise FileNotFoundError("FileNotFoundError: The required file does not exist.")

# Read the JSON file
try:
    with open(profile_info_path, 'r') as file:
        import json
        data = json.load(file)
except (json.JSONDecodeError, IOError) as e:
    raise ValueError(f"ValueError: Error reading the JSON file - {str(e)}")

# Extract the profile account insights
try:
    profile_account_insights = data.get('profile_account_insights', [])
except AttributeError:
    raise ValueError("ValueError: The JSON structure is not as expected.")

# Process each entry in the profile account insights
for entry in profile_account_insights:
    string_map_data = entry.get('string_map_data', {})
    
    # Extract the timestamp
    timestamp = string_map_data.get('Last Login', {}).get('timestamp')
    change_date = parse_timestamp(timestamp) if timestamp else None
    
    # Extract and store the changes
    for key, value in string_map_data.items():
        if key in ['First Country Code', 'First Close Friends Story Time', 'First Story Time', 'Has Shared Live Video', 'Last Login', 'Last Logout', 'Last Story Time']:
            continue  # Skip these keys as they are not relevant for the query
        new_value = value.get('value')
        changes.append([key, new_value, change_date])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Changed', 'New Value', 'Change Date'])
    writer.writerows(changes)