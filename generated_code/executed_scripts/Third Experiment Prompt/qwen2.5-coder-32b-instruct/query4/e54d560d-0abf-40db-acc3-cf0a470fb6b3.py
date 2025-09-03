import os
import csv

# Define the root directory
root_dir = "root_dir"

# Define the path to the file that might contain information about third-party apps/websites
file_path = os.path.join(root_dir, "apps_and_websites_off_of_instagram", "apps_and_websites", "no-data.txt")

# Initialize a list to store company names
company_names = []

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file and read its content
        with open(file_path, 'r') as file:
            content = file.read().strip()
        
        # If the file is empty or contains "no-data.txt", it means no companies have access
        if content == "":
            # No companies have access
            pass
        else:
            # If the file contains data, we need to parse it to extract company names
            # For this example, we assume the file contains company names, one per line
            company_names = content.splitlines()
    else:
        # If the file does not exist, we assume no companies have access
        pass

except FileNotFoundError as e:
    print(e)
    # Create an empty list of company names
    company_names = []

# Define the path to save the CSV file
csv_file_path = 'query_responses/results.csv'

# Ensure the directory exists
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

# Write the company names to the CSV file
with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the header
    csv_writer.writerow(['Company Name'])
    # Write the company names
    for company in company_names:
        csv_writer.writerow([company])

print(f"Results saved to {csv_file_path}")