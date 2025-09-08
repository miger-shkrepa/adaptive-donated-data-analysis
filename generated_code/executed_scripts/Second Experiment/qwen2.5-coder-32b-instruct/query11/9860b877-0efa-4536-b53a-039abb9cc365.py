import os
import csv

root_dir = "root_dir"

def get_account_names(file_path):
    try:
        with open(file_path, 'r') as file:
            import json
            data = json.load(file)
            accounts = set()
            for entry in data['impressions_history_posts_seen']:
                accounts.add(entry['string_map_data']['Author']['value'])
            return accounts
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file for viewed posts does not exist.")
    except ValueError:
        raise ValueError("ValueError: The file for viewed posts is not in a valid JSON format.")
    except KeyError:
        raise KeyError("KeyError: The file for viewed posts does not have the expected structure.")

def get_disliked_account_names(file_path):
    try:
        with open(file_path, 'r') as file:
            import json
            data = json.load(file)
            accounts = set()
            for entry in data['impressions_history_posts_not_interested']:
                accounts.add(entry['string_list_data'][1]['value'])
            return accounts
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file for disliked posts does not exist.")
    except ValueError:
        raise ValueError("ValueError: The file for disliked posts is not in a valid JSON format.")
    except KeyError:
        raise KeyError("KeyError: The file for disliked posts does not have the expected structure.")

def main():
    try:
        viewed_posts_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        disliked_posts_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_you\'re_not_interested_in.json')

        viewed_accounts = get_account_names(viewed_posts_path) if os.path.exists(viewed_posts_path) else set()
        disliked_accounts = get_disliked_account_names(disliked_posts_path) if os.path.exists(disliked_posts_path) else set()

        result_accounts = viewed_accounts - disliked_accounts

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in result_accounts:
                writer.writerow([account])

    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

if __name__ == "__main__":
    main()