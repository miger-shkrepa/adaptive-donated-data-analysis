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
    for root, dirs, files in os.walk(root_dir):
        if "personal_information" in dirs and "information_about_you" in os.listdir(os.path.join(root_dir, "personal_information")):
            for subroot, subdirs, subfiles in os.walk(os.path.join(root_dir, "personal_information", "information_about_you")):
                if "locations_of_interest.json" in subfiles:
                    with open(os.path.join(subroot, "locations_of_interest.json"), 'r') as f:
                        data = json.load(f)
                        for item in data["label_values"]:
                            if item["vec"]:
                                writer.writerow([item["label"], item["vec"][0]["value"], item["timestamp_value"]])

                elif "profile_based_in.json" in subfiles:
                    with open(os.path.join(subroot, "profile_based_in.json"), 'r') as f:
                        data = json.load(f)
                        for item in data["inferred_data_primary_location"]:
                            writer.writerow([item["string_map_data"]["City Name"]["value"], item["string_map_data"]["City Name"]["value"], item["string_map_data"]["City Name"]["timestamp"]])

        elif "personal_information" in dirs and "personal_information" in os.listdir(os.path.join(root_dir, "personal_information")):
            for subroot, subdirs, subfiles in os.walk(os.path.join(root_dir, "personal_information", "personal_information")):
                if "instagram_profile_information.json" in subfiles:
                    with open(os.path.join(subroot, "instagram_profile_information.json"), 'r') as f:
                        data = json.load(f)
                        for item in data["profile_account_insights"]:
                            writer.writerow([item["string_map_data"]["Name"]["value"], item["string_map_data"]["Name"]["value"], item["string_map_data"]["Name"]["timestamp"]])

                elif "note_interactions.json" in subfiles:
                    with open(os.path.join(subroot, "note_interactions.json"), 'r') as f:
                        data = json.load(f)
                        for item in data["profile_note_interactions"]:
                            writer.writerow([item["string_map_data"]["Last Notes Seen Time"]["value"], item["string_map_data"]["Last Notes Seen Time"]["value"], item["string_map_data"]["Last Notes Seen Time"]["timestamp"]])

                elif "personal_information.json" in subfiles:
                    with open(os.path.join(subroot, "personal_information.json"), 'r') as f:
                        data = json.load(f)
                        for item in data["profile_user"]:
                            writer.writerow([item["string_map_data"]["Name"]["value"], item["string_map_data"]["Name"]["value"], item["string_map_data"]["Name"]["timestamp"]])

                elif "professional_information.json" in subfiles:
                    with open(os.path.join(subroot, "professional_information.json"), 'r') as f:
                        data = json.load(f)
                        for item in data["profile_business"]:
                            writer.writerow([item["string_map_data"]["Name"]["value"], item["string_map_data"]["Name"]["value"], item["string_map_data"]["Name"]["timestamp"]])

                elif "profile_changes.json" in subfiles:
                    with open(os.path.join(subroot, "profile_changes.json"), 'r') as f:
                        data = json.load(f)
                        for item in data["profile_profile_change"]:
                            writer.writerow([item["string_map_data"]["Change Date"]["value"], item["string_map_data"]["New Value"]["value"], item["string_map_data"]["Change Date"]["timestamp"]])

# Close the CSV writer
csvfile.close()