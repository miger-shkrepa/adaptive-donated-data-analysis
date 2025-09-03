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
                # Check if the subdirectory contains Instagram-related data
                if "instagram" in subitem.lower() or "your_instagram_activity" in subitem.lower():
                    # Extract the company name from the subdirectory name
                    company_name = item
                    # Add the company name to the list
                    company_names.append(company_name)

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])  # header
    for company in company_names:
        writer.writerow([company])