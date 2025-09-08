import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the directory structure
for item in os.listdir(root_dir):
    # Check if the item is a directory
    if os.path.isdir(os.path.join(root_dir, item)):
        # Iterate over the subdirectories
        for subitem in os.listdir(os.path.join(root_dir, item)):
            # Check if the subitem is a directory
            if os.path.isdir(os.path.join(root_dir, item, subitem)):
                # Check if the subdirectory contains Instagram activity or information
                if subitem == "your_instagram_activity":
                    # Iterate over the files in the subdirectory
                    for file in os.listdir(os.path.join(root_dir, item, subitem)):
                        # Check if the file is a JSON file
                        if file.endswith(".json"):
                            # Open the JSON file
                            with open(os.path.join(root_dir, item, subitem, file), "r") as f:
                                # Read the JSON file
                                data = f.read()
                                # Check if the JSON file contains company names
                                if "Company Name" in data:
                                    # Extract the company names
                                    company_names.extend([line.split(",")[0] for line in data.splitlines() if line.startswith("Company Name")])

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    writer.writerows([(name,) for name in company_names])