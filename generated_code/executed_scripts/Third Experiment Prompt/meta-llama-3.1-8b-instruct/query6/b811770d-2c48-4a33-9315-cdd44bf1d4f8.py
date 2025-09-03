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

# Define the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Iterate over the directory structure
    for root, dirs, files in os.walk(root_dir):
        if "personal_information" in dirs and "information_about_you" in dirs:
            for file in files:
                if file == "profile_changes.json":
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as json_file:
                            data = json.load(json_file)
                            for item in data["profile_profile_change"]:
                                writer.writerow([item["string_map_data"]["Changed"]["value"], item["string_map_data"]["New Value"]["value"], item["string_map_data"]["Change Date"]["timestamp"]])
                    except FileNotFoundError:
                        print(f"Error: File '{file_path}' not found.")
                    except json.JSONDecodeError:
                        print(f"Error: Failed to parse JSON in file '{file_path}'.")
                    except KeyError:
                        print(f"Error: Missing key in JSON data in file '{file_path}'.")