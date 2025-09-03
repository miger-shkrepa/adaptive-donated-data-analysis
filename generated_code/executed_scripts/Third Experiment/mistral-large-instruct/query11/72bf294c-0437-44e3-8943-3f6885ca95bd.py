import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract viewed and liked accounts
def extract_accounts(root_dir):
    viewed_accounts = set()
    liked_accounts = set()

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Traverse the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        # Extract viewed accounts
                        if 'viewed_posts' in data:
                            for post in data['viewed_posts']:
                                viewed_accounts.add(post['account'])
                        # Extract liked accounts
                        if 'liked_posts' in data:
                            for post in data['liked_posts']:
                                liked_accounts.add(post['account'])
                except json.JSONDecodeError:
                    raise ValueError("Error: Invalid JSON format in file {}".format(file_path))

    # Find accounts that were viewed but not liked
    accounts_viewed_not_liked = viewed_accounts - liked_accounts

    return accounts_viewed_not_liked

# Function to write the results to a CSV file
def write_to_csv(accounts, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['Account']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for account in accounts:
                writer.writerow({'Account': account})
    except Exception as e:
        raise IOError("Error: Failed to write to CSV file. {}".format(str(e)))

# Main function
def main():
    try:
        accounts = extract_accounts(root_dir)
        write_to_csv(accounts, output_csv)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()