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
                        if "profile_changes.json" in file:
                            for item in data["profile_profile_change"]:
                                writer.writerow([item["Changed"], item["New Value"], item["Change Date"]])
                        elif "personal_information" in file and "profile_changes.json" not in file:
                            for item in data["profile_profile_change"]:
                                writer.writerow([item["Changed"], item["New Value"], item["Change Date"]])
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON file: {e}")
                except KeyError as e:
                    print(f"Error accessing key: {e}")
                except Exception as e:
                    print(f"Error processing file: {e}")

# Print a message to indicate that the script has finished
print("Script finished.")