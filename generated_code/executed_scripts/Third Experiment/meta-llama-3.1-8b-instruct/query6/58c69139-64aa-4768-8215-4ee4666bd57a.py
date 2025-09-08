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

            # Check if the JSON file contains the required data
            if "personal_information" in data and "instagram_profile_information.json" in data["personal_information"]:
                # Load the Instagram profile information
                instagram_data = data["personal_information"]["instagram_profile_information.json"]

                # Check if the Instagram profile information contains the required data
                if "profile_account_insights" in instagram_data and instagram_data["profile_account_insights"]:
                    # Iterate over the account insights
                    for insight in instagram_data["profile_account_insights"]:
                        # Check if the insight contains the required data
                        if "string_map_data" in insight and "First Name" in insight["string_map_data"] and "Last Name" in insight["string_map_data"] and "Phone Number" in insight["string_map_data"] and "Email" in insight["string_map_data"]:
                            # Extract the first name, last name, phone number, and email
                            first_name = insight["string_map_data"]["First Name"]["value"]
                            last_name = insight["string_map_data"]["Last Name"]["value"]
                            phone_number = insight["string_map_data"]["Phone Number"]["value"]
                            email = insight["string_map_data"]["Email"]["value"]

                            # Extract the change date
                            change_date = datetime.datetime.fromtimestamp(int(insight["string_map_data"]["Last Story Time"]["timestamp"])).strftime('%Y-%m-%d')

                            # Add the change to the list
                            changes.append([f"{first_name} {last_name}", phone_number, email, change_date])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)