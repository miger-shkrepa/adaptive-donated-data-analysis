import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the user engagement dictionary
user_engagement = {}

# Iterate over the JSON files in the directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Iterate over the JSON data
            for item in data:
                # Check if the item has a 'string_map_data' key
                if 'string_map_data' in item:
                    # Iterate over the string map data
                    for key, value in item['string_map_data'].items():
                        # Check if the key is 'Last Story Time'
                        if key == 'Last Story Time':
                            # Get the user name
                            user_name = item['title']

                            # Check if the user is already in the user engagement dictionary
                            if user_name in user_engagement:
                                # Increment the engagement count
                                user_engagement[user_name] += 1
                            else:
                                # Add the user to the user engagement dictionary
                                user_engagement[user_name] = 1

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create the CSV writer
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(['User', 'Times Engaged'])

    # Iterate over the user engagement dictionary
    for user, engagement in user_engagement.items():
        # Write the user and engagement count to the CSV file
        writer.writerow([user, engagement])