import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Check if the JSON data contains the required information
            if "restricted_accounts" in data:
                # Extract the company name from the JSON data
                company_name = "Restricted Accounts"
                # Add the company name to the list
                company_names.append(company_name)
            elif "monetization" in data:
                # Extract the company name from the JSON data
                company_name = "Monetization"
                # Add the company name to the list
                company_names.append(company_name)
            elif "secret_conversations" in data:
                # Extract the company name from the JSON data
                company_name = "Secret Conversations"
                # Add the company name to the list
                company_names.append(company_name)

# Create a CSV file to store the company names
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Company Name"])
    # Write the company names
    writer.writerows([[company_name] for company_name in company_names])