import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate through the directory structure
for item in os.listdir(root_dir):
    item_path = os.path.join(root_dir, item)
    if os.path.isfile(item_path):
        # Check if the file is a JSON file
        if item.endswith(".json"):
            with open(item_path, 'r') as file:
                data = file.read()
                # Check if the JSON file contains the required structure
                if "your_instagram_activity" in data:
                    # Extract the company name from the JSON file
                    company_name = "Instagram"
                    company_names.append(company_name)
                elif "personal_information" in data:
                    # Extract the company name from the JSON file
                    company_name = "Your Company"
                    company_names.append(company_name)
    elif os.path.isdir(item_path):
        # Recursively iterate through the subdirectories
        for subitem in os.listdir(item_path):
            subitem_path = os.path.join(item_path, subitem)
            if os.path.isfile(subitem_path):
                # Check if the file is a JSON file
                if subitem.endswith(".json"):
                    with open(subitem_path, 'r') as file:
                        data = file.read()
                        # Check if the JSON file contains the required structure
                        if "your_instagram_activity" in data:
                            # Extract the company name from the JSON file
                            company_name = "Instagram"
                            company_names.append(company_name)
                        elif "personal_information" in data:
                            # Extract the company name from the JSON file
                            company_name = "Your Company"
                            company_names.append(company_name)

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])  # Write the column headers
    for company_name in company_names:
        writer.writerow([company_name])