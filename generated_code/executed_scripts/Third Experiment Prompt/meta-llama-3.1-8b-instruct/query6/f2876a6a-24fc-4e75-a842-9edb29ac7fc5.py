import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = "query_responses/results.csv"

# Define the CSV writer
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "personal_information.json":
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, "r") as json_file:
                        data = json.load(json_file)
                        if "profile_user" in data:
                            for item in data["profile_user"]:
                                for key, value in item.items():
                                    if key == "string_map_data":
                                        for k, v in value.items():
                                            if k in ["Benutzername", "E-Mail-Adresse", "Geburtsdatum", "Geschlecht", "Name", "Privates Konto", "Telefonnummer bestätigt"]:
                                                writer.writerow([k, v["value"], ""])
                        elif "profile_business" in data:
                            for item in data["profile_business"]:
                                for key, value in item.items():
                                    if key == "string_map_data":
                                        for k, v in value.items():
                                            if k in ["Name", "E-Mail-Adresse", "Geburtsdatum", "Geschlecht", "Name", "Privates Konto", "Telefonnummer bestätigt"]:
                                                writer.writerow([k, v["value"], ""])
                        elif "profile_profile_change" in data:
                            for item in data["profile_profile_change"]:
                                for key, value in item.items():
                                    if key == "string_map_data":
                                        for k, v in value.items():
                                            if k in ["Change Date", "Changed", "New Value", "Vorheriger Wert"]:
                                                writer.writerow([k, v["value"], v["href"]])
                except FileNotFoundError:
                    print(f"Error: File '{filepath}' not found.")
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON in file '{filepath}'.")