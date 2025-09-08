import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Initialize an empty set to store the unique profiles that do not follow back
no_follow_back = set()

# Iterate over the 'your_instagram_activity' directory
for activity in os.listdir(root_dir + "/your_instagram_activity"):
    # Check if the 'likes' or 'saved' directory exists
    if activity in ["likes", "saved"]:
        # Iterate over the JSON files in the 'likes' or 'saved' directory
        for file in os.listdir(root_dir + "/your_instagram_activity/" + activity):
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Load the JSON file
                with open(root_dir + "/your_instagram_activity/" + activity + "/" + file, "r") as f:
                    data = json.load(f)
                # Check if the 'structure' key exists in the JSON file
                if "structure" in data:
                    # Iterate over the 'likes_media_likes' or 'saved_saved_media' list
                    for item in data["structure"].get(activity + "_media", []):
                        # Check if the 'string_list_data' or 'string_map_data' list exists
                        if "string_list_data" in item:
                            # Iterate over the 'string_list_data' list
                            for profile in item.get("string_list_data", []):
                                # Check if the 'href' field exists
                                if "href" in profile:
                                    # Add the profile to the 'no_follow_back' set
                                    no_follow_back.add(profile["href"])
                        elif "string_map_data" in item:
                            # Iterate over the 'string_map_data' dictionary
                            for profile in item.get("string_map_data", {}).values():
                                # Check if the 'href' field exists
                                if "href" in profile:
                                    # Add the profile to the 'no_follow_back' set
                                    no_follow_back.add(profile["href"])

# Write the 'no_follow_back' set to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Profile"])  # Write the header
    writer.writerows([profile for profile in no_follow_back])  # Write the unique profiles