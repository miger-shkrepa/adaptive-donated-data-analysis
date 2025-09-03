import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the user and times engaged
users = []
times_engaged = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Parse the JSON data
            import json
            parsed_data = json.loads(data)
            # Check if the JSON data contains the required information
            if 'personal_information' in parsed_data and 'instagram_profile_information.json' in parsed_data['personal_information']:
                # Extract the user and times engaged from the JSON data
                user = parsed_data['personal_information']['instagram_profile_information.json']['profile_account_insights'][0]['string_map_data']['First Story Time']['value']
                times_engaged.append(int(parsed_data['personal_information']['instagram_profile_information.json']['profile_account_insights'][0]['string_map_data']['First Story Time']['timestamp']))
                users.append(user)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, time in zip(users, times_engaged):
        writer.writerow([user, time])