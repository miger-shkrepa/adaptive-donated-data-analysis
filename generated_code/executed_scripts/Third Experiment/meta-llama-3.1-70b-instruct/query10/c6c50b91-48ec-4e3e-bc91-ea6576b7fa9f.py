import os
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        for filename in os.listdir(os.path.join(root_dir, 'likes')):
            if filename == 'liked_comments.json':
                with open(os.path.join(root_dir, 'likes', filename), 'r') as file:
                    # Assuming the JSON file has a similar structure to the provided context
                    # and that the 'href' field contains the account information
                    for line in file:
                        # Simple parsing, may need to be adjusted based on the actual JSON structure
                        if 'href' in line:
                            account = line.split('href": ')[1].split('"')[0]
                            if account in account_views:
                                account_views[account]['Post Views'] += 1
                            else:
                                account_views[account] = {'Post Views': 1, 'Video Views': 0}
        for filename in os.listdir(os.path.join(root_dir, 'instagram_live')):
            if filename != 'no-data.txt':
                with open(os.path.join(root_dir, 'instagram_live', filename), 'r') as file:
                    # Assuming the file contains video view information
                    for line in file:
                        # Simple parsing, may need to be adjusted based on the actual file structure
                        if 'account' in line:
                            account = line.split('account: ')[1].split('\n')[0]
                            if account in account_views:
                                account_views[account]['Video Views'] += 1
                            else:
                                account_views[account] = {'Post Views': 0, 'Video Views': 1}
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))
    return account_views

def save_to_csv(account_views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in account_views.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

def main():
    try:
        account_views = get_account_views(root_dir)
        save_to_csv(account_views)
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()