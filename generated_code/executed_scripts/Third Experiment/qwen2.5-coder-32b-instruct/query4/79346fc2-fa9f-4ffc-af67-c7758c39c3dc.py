import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a list to store company names
company_names = []

# Check for the presence of the 'messages' directory
messages_dir = os.path.join(root_dir, "your_instagram_activity", "messages")
if os.path.exists(messages_dir):
    # Assuming the presence of 'messages' directory indicates some form of third-party access
    company_names.append("Third-Party Messaging Platforms")

# Prepare the CSV file path
csv_file_path = 'query_responses/results.csv'

# Ensure the directory for the CSV file exists
os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

# Write the results to a CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name"])  # Write the header
    for company in company_names:
        writer.writerow([company])  # Write each company name

print(f"Results have been saved to {csv_file_path}")