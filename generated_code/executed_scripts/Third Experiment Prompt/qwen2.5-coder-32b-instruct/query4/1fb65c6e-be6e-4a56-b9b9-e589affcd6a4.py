import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to check if a file exists and is a file
def file_exists(file_path):
    return os.path.isfile(file_path)

# Function to read JSON file and extract company names (if any)
def extract_company_names(json_file_path):
    company_names = []
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Assuming we need to search for 'company' in the JSON structure
            # This is a placeholder as there is no actual company data in the provided structure
            # In a real scenario, you would parse the JSON data to find company names
            # For demonstration, we will just return an empty list
            return company_names
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {json_file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {json_file_path} is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while reading {json_file_path}: {str(e)}")

# Define paths to the JSON files
liked_posts_json_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
saved_posts_json_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Initialize a set to store unique company names
company_names_set = set()

# Check and extract company names from liked_posts.json if it exists
if file_exists(liked_posts_json_path):
    company_names_set.update(extract_company_names(liked_posts_json_path))

# Check and extract company names from saved_posts.json if it exists
if file_exists(saved_posts_json_path):
    company_names_set.update(extract_company_names(saved_posts_json_path))

# Prepare the output CSV file path
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the company names to the CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Company Name"])
    for company_name in company_names_set:
        csvwriter.writerow([company_name])

print(f"Results have been written to {output_csv_path}")