import csv
import json

# Define the root directory
root_dir = "root_dir"

try:
    # Check if the root directory exists
    import os
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Initialize the list of companies
companies = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), "r") as f:
            data = json.load(f)
            # Check if the JSON file contains the required structure
            if "type" in data and data["type"] == "json":
                # Check if the JSON file contains the required structure
                if "structure" in data:
                    # Check if the JSON file contains the required structure
                    if "likes" in data["structure"]:
                        # Check if the JSON file contains the required structure
                        if "liked_posts.json" in data["structure"]["likes"]:
                            # Extract the company name from the JSON file
                            company = data["structure"]["likes"]["liked_posts.json"]["title"]
                            companies.append(company)
                    elif "saved" in data["structure"]:
                        # Check if the JSON file contains the required structure
                        if "saved_posts.json" in data["structure"]["saved"]:
                            # Extract the company name from the JSON file
                            company = data["structure"]["saved"]["saved_posts.json"]["title"]
                            companies.append(company)

# Write the list of companies to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    writer.writerows([company for company in companies])