import os
import json
import csv

root_dir = "root_dir"

def get_account_info(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty set to store the accounts the user has viewed posts from
        viewed_accounts = set()

        # Initialize an empty set to store the accounts the user has liked posts from
        liked_accounts = set()

        # Iterate over the files in the 'ads_information' directory
        ads_info_dir = os.path.join(root_dir, 'ads_information')
        if os.path.exists(ads_info_dir):
            for filename in os.listdir(ads_info_dir):
                if filename == 'posts_viewed.json':
                    # Open the 'posts_viewed.json' file and load the data
                    with open(os.path.join(ads_info_dir, filename), 'r') as file:
                        data = json.load(file)
                        # Iterate over the posts viewed by the user
                        for post in data['impressions_history_posts_seen']:
                            # Add the author of the post to the set of viewed accounts
                            viewed_accounts.add(post['string_map_data']['Author']['value'])

                elif filename == 'posts_you_re_not_interested_in.json':
                    # Open the 'posts_you_re_not_interested_in.json' file and load the data
                    with open(os.path.join(ads_info_dir, filename), 'r') as file:
                        data = json.load(file)
                        # Iterate over the posts the user is not interested in
                        for post in data['impressions_history_posts_not_interested']:
                            # Add the author of the post to the set of liked accounts
                            liked_accounts.add(post['string_list_data'][1]['value'])

        # Calculate the difference between the viewed accounts and the liked accounts
        not_liked_accounts = viewed_accounts - liked_accounts

        # Return the not liked accounts
        return not_liked_accounts

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(accounts, filename):
    try:
        # Open the CSV file and write the accounts to it
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Account'])
            for account in accounts:
                writer.writerow([account])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the account information
        accounts = get_account_info(root_dir)

        # Write the account information to a CSV file
        write_to_csv(accounts, 'query_responses/results.csv')

    except FileNotFoundError as e:
        # If the root directory does not exist, write an empty CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Account'])
        raise ValueError("Error: " + str(e))

    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()