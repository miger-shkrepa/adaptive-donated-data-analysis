import csv
import os

def get_account_from_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = f.read()
            return data.split('"Account": "')[1].split('"')[0]
    except Exception as e:
        raise ValueError("Error: Unable to parse JSON file.")

def get_account_from_directory(directory):
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    account = get_account_from_json(file_path)
                    return account
    except Exception as e:
        raise FileNotFoundError("Error: The root directory does not exist.")

def get_accounts_with_viewed_posts_but_not_liked(directory):
    try:
        accounts = set()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    if "profile_user" in open(file_path, 'r').read():
                        account = get_account_from_json(file_path)
                        accounts.add(account)
        return accounts
    except Exception as e:
        raise ValueError("Error: Unable to parse JSON file.")

def main():
    root_dir = "root_dir"
    accounts = get_accounts_with_viewed_posts_but_not_liked(root_dir)
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

if __name__ == "__main__":
    main()