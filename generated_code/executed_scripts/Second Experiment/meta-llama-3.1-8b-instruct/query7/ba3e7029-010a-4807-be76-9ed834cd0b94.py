import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if 'personal_information' in data and 'instagram_profile_information.json' in data['personal_information']:
                # Extract the required information
                profile_account_insights = data['personal_information']['instagram_profile_information.json']['structure']['profile_account_insights']

                # Iterate over the profile account insights
                for insight in profile_account_insights:
                    # Check if the insight contains the required information
                    if 'string_map_data' in insight and 'First Story Time' in insight['string_map_data'] and 'Last Story Time' in insight['string_map_data']:
                        # Extract the user and times engaged
                        user = insight['title']
                        times_engaged = insight['string_map_data']['Last Story Time']['value'] - insight['string_map_data']['First Story Time']['value']

                        # Append the result to the list
                        results.append((user, times_engaged))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Times Engaged'])
    writer.writerows(results)

# Check if the CSV file was written successfully
if not os.path.exists('query_responses/results.csv'):
    raise ValueError("ValueError: The CSV file was not written successfully.")