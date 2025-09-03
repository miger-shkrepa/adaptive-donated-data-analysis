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
for dir, _, files in os.walk(root_dir):
    # Check if the current directory is 'your_instagram_activity'
    if dir.endswith('your_instagram_activity'):
        # Iterate over the files in the current directory
        for file in files:
            # Check if the file is a JSON file
            if file.endswith('.json'):
                # Open the file and read its contents
                with open(os.path.join(dir, file), 'r') as f:
                    data = f.read()
                    # Parse the JSON data
                    import json
                    data = json.loads(data)
                    # Check if the file contains information about companies
                    if 'companies' in data:
                        # Extract the company names
                        company_names.extend([company['name'] for company in data['companies']])

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name'])
    writer.writerows([[company] for company in company_names])