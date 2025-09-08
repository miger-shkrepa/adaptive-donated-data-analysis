import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the directory structure
for root, dirs, files in os.walk(root_dir):
    if "your_instagram_activity" in dirs:
        for subroot, subdirs, subfiles in os.walk(os.path.join(root_dir, "your_instagram_activity")):
            if "monetization" in subdirs:
                for file in subfiles:
                    if file.endswith(".json"):
                        try:
                            with open(os.path.join(subroot, file), 'r') as f:
                                data = json.load(f)
                                if "monetization_eligibility" in data:
                                    for item in data["monetization_eligibility"]:
                                        company_names.append(item["title"])
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON file: {e}")
                        except FileNotFoundError as e:
                            print(f"Error: {e}")

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    writer.writerows([[company] for company in company_names])