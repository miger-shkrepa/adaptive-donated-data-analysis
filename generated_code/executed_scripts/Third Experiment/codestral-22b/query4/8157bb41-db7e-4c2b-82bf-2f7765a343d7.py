import os
import csv
import json

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store company names
company_names = []

# Define the path to the Instagram activity directory
instagram_activity_dir = os.path.join(root_dir, "your_instagram_activity")

# Check if the Instagram activity directory exists
if os.path.exists(instagram_activity_dir):
    # Iterate through all the JSON files in the Instagram activity directory
    for filename in os.listdir(instagram_activity_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(instagram_activity_dir, filename)
            # Open the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Extract the company names from the JSON data
                for item in data:
                    if "Media Owner" in item["string_map_data"]:
                        company_names.append(item["string_map_data"]["Media Owner"]["value"])

# Define the path to the Instagram information directory
instagram_info_dir = os.path.join(root_dir, "accounts_center", "instagram_information")

# Check if the Instagram information directory exists
if os.path.exists(instagram_info_dir):
    # Iterate through all the JSON files in the Instagram information directory
    for filename in os.listdir(instagram_info_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(instagram_info_dir, filename)
            # Open the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Extract the company names from the JSON data
                for item in data:
                    if "Name" in item["string_map_data"]:
                        company_names.append(item["string_map_data"]["Name"]["value"])

# Remove duplicates from the company names list
company_names = list(set(company_names))

# Save the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name"])
    for name in company_names:
        writer.writerow([name])