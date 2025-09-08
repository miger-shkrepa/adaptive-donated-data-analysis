import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = "query_responses/results.csv"

# Initialize the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Iterate over the directory structure
    for dir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(dir, file)
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        if "personal_information" in data and "profile_changes" in data["personal_information"]:
                            for change in data["personal_information"]["profile_changes"]["profile_profile_change"]:
                                if "Changed" in change["string_map_data"] and "New Value" in change["string_map_data"] and "Change Date" in change["string_map_data"]:
                                    writer.writerow([change["string_map_data"]["Changed"]["value"], change["string_map_data"]["New Value"]["value"], change["string_map_data"]["Change Date"]["value"]])
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON file: {e}")
                except KeyError as e:
                    print(f"Error accessing key: {e}")