import os
import csv
import json

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    companies_with_access = []

    # Check if the required directory exists
    policy_updates_dir = os.path.join(root_dir, "logged_information", "policy_updates_and_permissions")
    if not os.path.exists(policy_updates_dir):
        # If the directory does not exist, return a CSV with only the header
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
        raise FileNotFoundError("FileNotFoundError: The required directory for policy updates and permissions does not exist.")

    # Check if the required file exists
    policy_updates_file = os.path.join(policy_updates_dir, "no-data.txt")
    if not os.path.exists(policy_updates_file):
        # If the file does not exist, return a CSV with only the header
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
        raise FileNotFoundError("FileNotFoundError: The required file for policy updates and permissions does not exist.")

    # Since the file is "no-data.txt", it indicates no data is available. Thus, no companies have access.
    # Write the header to the CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])

except Exception as e:
    print(f"Error: {e}")