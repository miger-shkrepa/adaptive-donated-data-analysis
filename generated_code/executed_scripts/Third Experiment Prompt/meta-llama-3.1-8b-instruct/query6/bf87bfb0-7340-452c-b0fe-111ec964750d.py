import csv
import os
import datetime
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Iterate over the 'preferences' directory
    for filename in os.listdir(os.path.join(root_dir, "preferences", "settings")):
        if filename.endswith(".json"):
            filepath = os.path.join(root_dir, "preferences", "settings", filename)
            try:
                with open(filepath, 'r') as json_file:
                    data = json.load(json_file)
                    if "structure" in data:
                        for item in data["structure"]:
                            if "string_map_data" in item:
                                for key, value in item["string_map_data"].items():
                                    if value["value"] != "":
                                        writer.writerow([key, value["value"], datetime.date.today().strftime("%Y-%m-%d")])
                    else:
                        # If 'structure' key is missing, treat it as an empty list
                        writer.writerow(["", "", datetime.date.today().strftime("%Y-%m-%d")])
            except FileNotFoundError:
                print(f"Error: The file '{filename}' does not exist.")
                writer.writerow(["", "", datetime.date.today().strftime("%Y-%m-%d")])
            except ValueError:
                print(f"Error: The file '{filename}' is not a valid JSON file.")
                writer.writerow(["", "", datetime.date.today().strftime("%Y-%m-%d")])