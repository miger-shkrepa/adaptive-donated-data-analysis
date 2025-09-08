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
    # Check if the item is a directory
    if os.path.isdir(os.path.join(root_dir, item)):
        # Iterate through the subdirectories
        for subitem in os.listdir(os.path.join(root_dir, item)):
            # Check if the subitem is a JSON file
            if subitem.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, item, subitem), "r") as f:
                    # Load the JSON data
                    data = json.load(f)
                    # Check if the JSON data contains the required information
                    if "relationships_following" in data["structure"]:
                        # Extract the company name from the JSON data
                        company_name = data["structure"]["relationships_following"][0]["title"]
                        # Add the company name to the list
                        company_names.append(company_name)

# Create a CSV writer
with open("query_responses/results.csv", "w", newline="") as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Company Name"])
    # Write the company names to the CSV file
    writer.writerows([[company_name] for company_name in company_names])

print("Query completed successfully.")