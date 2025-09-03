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
    # Check if the item is a file
    if os.path.isfile(os.path.join(root_dir, item)):
        # Check if the file is a JSON file
        if item.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(root_dir, item), 'r') as f:
                # Load the JSON data
                data = json.load(f)
                # Check if the JSON data contains information about Instagram activity
                if "your_instagram_activity" in data:
                    # Extract the company name from the JSON data
                    company_name = data["your_instagram_activity"]["title"]
                    # Add the company name to the list
                    company_names.append(company_name)

# Create a CSV file to store the results
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Company Name"])
    # Write the company names to the CSV file
    for company_name in company_names:
        writer.writerow([company_name])

print("Query completed successfully.")