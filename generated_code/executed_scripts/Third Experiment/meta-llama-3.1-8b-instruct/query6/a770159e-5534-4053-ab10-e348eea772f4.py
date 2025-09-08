import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the changes
changes = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if 'followers_and_following' in data and 'followers_1.json' in data['followers_and_following']:
                # Iterate over the followers
                for follower in data['followers_and_following']['followers_1.json']['structure']:
                    # Check if the follower has a name, phone, or email
                    if 'title' in follower and 'string_list_data' in follower and any('value' in item for item in follower['string_list_data']):
                        # Extract the name, phone, and email
                        name = None
                        phone = None
                        email = None
                        for item in follower['string_list_data']:
                            if 'value' in item and item['value'] == 'str':
                                if 'title' in item and item['title'] == 'str':
                                    name = item['value']
                                elif 'title' in item and item['title'] == 'int':
                                    phone = item['value']
                                elif 'title' in item and item['title'] == 'str':
                                    email = item['value']

                        # Add the change to the list
                        changes.append((name, phone, email, datetime.date.today().strftime("%Y-%m-%d")))

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Changed', 'New Value', 'Change Date'])
    writer.writerows(changes)