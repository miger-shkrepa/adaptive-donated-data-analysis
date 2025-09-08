import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if 'message_requests' in data and 'participants' in data['message_requests']:
                # Iterate over the participants
                for participant in data['message_requests']['participants']:
                    # Check if the participant is not the user and does not follow the user back
                    if participant['name'] != 'user' and not any(p['name'] == 'user' for p in data['message_requests']['participants']):
                        # Add the participant to the list of profiles
                        profiles.append(participant['name'])

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(['Profile'])

    # Write the profiles to the CSV file
    for profile in profiles:
        writer.writerow([profile])