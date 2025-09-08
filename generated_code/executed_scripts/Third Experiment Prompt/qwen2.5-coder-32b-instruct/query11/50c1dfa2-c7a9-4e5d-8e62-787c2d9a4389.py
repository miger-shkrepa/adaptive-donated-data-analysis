import os
import csv

# Define the root directory
root_dir = "root_dir"

# Define the paths to the required files
posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")

# Initialize sets to store account names
viewed_accounts = set()
liked_accounts = set()

# Function to read JSON file and extract account names
def extract_accounts_from_json(file_path, key):
    if not os.path.exists(file_path):
        return set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = eval(file.read())
            accounts = set()
            for item in data:
                if 'string_map_data' in item and key in item['string_map_data']:
                    accounts.add(item['string_map_data'][key]['value'])
            return accounts
    except Exception as e:
        raise ValueError(f"ValueError: Error reading {file_path}: {e}")

# Extract viewed accounts
viewed_accounts = extract_accounts_from_json(posts_viewed_path, "Author")

# Extract liked accounts
liked_accounts = extract_accounts_from_json(liked_posts_path, "string_list_data")

# Find accounts viewed but not liked
result_accounts = viewed_accounts - liked_accounts

# Define the output CSV file path
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the result to a CSV file
try:
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])
        for account in result_accounts:
            writer.writerow([account])
except Exception as e:
    raise ValueError(f"ValueError: Error writing to {output_csv_path}: {e}")