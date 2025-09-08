import csv
import os
import json

def get_login_info(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty list to store the login information
        login_info = []

        # Iterate over each file in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename), 'r') as file:
                    # Load the JSON data
                    data = json.load(file)

                    # Check if the JSON file contains login information
                    if "login_and_profile_creation" in data:
                        # Iterate over each login activity
                        for login_activity in data["login_and_profile_creation"]["login_activity"]["account_history_login_history"]:
                            # Extract the device ID and login time
                            device_id = login_activity["string_map_data"]["User Agent"]["value"]
                            login_time = login_activity["string_map_data"]["Time"]["value"]

                            # Append the login information to the list
                            login_info.append([device_id, login_time])

        # Return the login information
        return login_info

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the data.") from e

def write_to_csv(data):
    try:
        # Open the CSV file for writing
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            # Create a CSV writer
            writer = csv.writer(csvfile)

            # Write the header row
            writer.writerow(["Device ID", "Login Time"])

            # Write each row of data
            for row in data:
                writer.writerow(row)

    except Exception as e:
        raise ValueError("ValueError: An error occurred while writing to the CSV file.") from e

# Declare the variable referring to the file input
root_dir = "root_dir"

# Get the login information
login_info = get_login_info(root_dir)

# Write the login information to a CSV file
write_to_csv(login_info)