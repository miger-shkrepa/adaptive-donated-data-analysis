import csv
import os

# Define the root directory
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
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if "apps_and_websites_off_of_instagram" in data and "apps_and_websites" in data["apps_and_websites_off_of_instagram"] and "your_activity_off_meta_technologies.json" in data["apps_and_websites"]:
                # Extract the company name from the JSON data
                company_name = data["apps_and_websites_off_of_instagram"]["apps_and_websites"]["your_activity_off_meta_technologies.json"]["structure"]["apps_and_websites_off_meta_activity"][0]["name"]

                # Add the company name to the list
                company_names.append(company_name)

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])  # Write the column headers
    writer.writerows([[company_name] for company_name in company_names])  # Write the company names