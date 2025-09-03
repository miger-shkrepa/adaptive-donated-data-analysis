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
                    # Extract the user and times engaged
                    user = insight['string_map_data']['First Story Time']['value']
                    times_engaged = 0

                    # Check if the user has engaged with any stories
                    if 'First Story Time' in insight['string_map_data']:
                        times_engaged = 1

                    # Append the result to the list
                    results.append([user, times_engaged])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])  # header
    writer.writerows(results)

print("Results written to query_responses/results.csv")