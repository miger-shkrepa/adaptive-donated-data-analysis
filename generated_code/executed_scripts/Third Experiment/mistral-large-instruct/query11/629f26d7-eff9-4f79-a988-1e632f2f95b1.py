import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: ValueError: The file {file_path} is not a valid JSON file.")

# Function to get viewed accounts
def get_viewed_accounts(directory):
    viewed_accounts = set()
    viewed_file = os.path.join(directory, 'shopping', 'recently_viewed_items.json')
    if os.path.exists(viewed_file):
        data = read_json_file(viewed_file)
        for item in data.get('checkout_saved_recently_viewed_products', []):
            viewed_accounts.add(item['string_map_data']['Merchant Name']['value'])
    return viewed_accounts

# Function to get liked accounts
def get_liked_accounts(directory):
    liked_accounts = set()
    liked_file = os.path.join(directory, 'likes', 'liked_posts.json')
    if os.path.exists(liked_file):
        data = read_json_file(liked_file)
        for item in data.get('likes_media_likes', []):
            liked_accounts.add(item['title'])
    return liked_accounts

# Main function to get accounts viewed but not liked
def get_viewed_but_not_liked_accounts(directory):
    viewed_accounts = get_viewed_accounts(directory)
    liked_accounts = get_liked_accounts(directory)
    return viewed_accounts - liked_accounts

# Write the results to a CSV file
def write_to_csv(accounts, file_path):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise ValueError(f"Error: ValueError: Failed to write to CSV file. {str(e)}")

# Main execution
if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: FileNotFoundError: The root directory does not exist.")

    viewed_but_not_liked_accounts = get_viewed_but_not_liked_accounts(root_dir)

    if not os.path.exists('query_responses'):
        os.makedirs('query_responses')

    write_to_csv(viewed_but_not_liked_accounts, output_csv)