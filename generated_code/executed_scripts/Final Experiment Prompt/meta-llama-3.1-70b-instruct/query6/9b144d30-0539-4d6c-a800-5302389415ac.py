import json
import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

# Initialize the CSV data
csv_data = [["Changed", "New Value", "Change Date"]]

# Check if the JSON file exists
if os.path.exists(json_file_path):
    try:
        # Open and load the JSON file
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        # Iterate over the profile changes
        for change in data["profile_profile_change"]:
            # Extract the changed field, new value, and change date
            changed = change["string_map_data"]["Changed"]["value"]
            new_value = change["string_map_data"]["New Value"]["value"]
            change_date_timestamp = change["string_map_data"]["Change Date"]["timestamp"]

            # Convert the change date timestamp to a date string
            from datetime import datetime
            change_date = datetime.utcfromtimestamp(change_date_timestamp).strftime("%Y-%m-%d")

            # Append the data to the CSV data
            csv_data.append([changed, new_value, change_date])

    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not valid.")
    except KeyError as e:
        raise ValueError(f"Error: The JSON file is missing a required key: {e}")

# Save the CSV data to a file
with open("query_responses/results.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(csv_data)