import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to extract viewed accounts from recently_viewed_items.json
def get_viewed_accounts(root_dir):
    viewed_accounts = set()
    file_path = os.path.join(root_dir, "your_instagram_activity", "shopping", "recently_viewed_items.json")
    if os.path.exists(file_path):
        data = read_json_file(file_path)
        for item in data.get("checkout_saved_recently_viewed_products", []):
            merchant_name = item.get("string_map_data", {}).get("Merchant Name", {}).get("value")
            if merchant_name:
                viewed_accounts.add(merchant_name)
    return viewed_accounts

# Function to extract liked accounts from liked_posts.json
def get_liked_accounts(root_dir):
    liked_accounts = set()
    file_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
    if os.path.exists(file_path):
        data = read_json_file(file_path)
        for item in data.get("likes_media_likes", []):
            for entry in item.get("string_list_data", []):
                value = entry.get("value")
                if value:
                    liked_accounts.add(value)
    return liked_accounts

# Main function to find accounts viewed but not liked
def find_viewed_but_not_liked_accounts(root_dir):
    try:
        viewed_accounts = get_viewed_accounts(root_dir)
        liked_accounts = get_liked_accounts(root_dir)
        viewed_but_not_liked_accounts = viewed_accounts - liked_accounts
        return viewed_but_not_liked_accounts
    except Exception as e:
        print(f"Error: {e}")
        return set()

# Write the result to a CSV file
def write_to_csv(accounts, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise Exception(f"Error: {e}")

# Define the output path
output_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Find and write the accounts
viewed_but_not_liked_accounts = find_viewed_but_not_liked_accounts(root_dir)
write_to_csv(viewed_but_not_liked_accounts, output_path)