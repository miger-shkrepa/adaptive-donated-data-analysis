import csv
import os

root_dir = "root_dir"

def get_account_from_posts_viewed(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            accounts = []
            for post in data['impressions_history_posts_seen']:
                author = post['string_map_data']['Author']['value']
                accounts.append(author)
            return accounts
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def get_account_from_posts_you_re_not_interested_in(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            accounts = []
            for post in data['impressions_history_posts_not_interested']:
                for timestamp in post['string_list_data']:
                    if 'href' in timestamp:
                        accounts.append(timestamp['href'])
            return accounts
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def get_accounts():
    accounts = set()
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'posts_viewed.json':
                accounts.update(get_account_from_posts_viewed(os.path.join(root, file)))
            elif file == 'posts_you\'re_not_interested_in.json':
                accounts.update(get_account_from_posts_you_re_not_interested_in(os.path.join(root, file)))
    return accounts

def save_to_csv(accounts):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])
        for account in accounts:
            writer.writerow([account])

try:
    accounts = get_accounts()
    save_to_csv(accounts)
except Exception as e:
    print(f"Error: {str(e)}")