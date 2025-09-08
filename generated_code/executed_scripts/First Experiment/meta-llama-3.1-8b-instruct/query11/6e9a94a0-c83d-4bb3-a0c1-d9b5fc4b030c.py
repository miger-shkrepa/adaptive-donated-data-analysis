import csv
import os

def get_account_info(root_dir):
    try:
        # Initialize an empty list to store account information
        accounts = []

        # Iterate over each file in the root directory
        for filename in os.listdir(root_dir):
            # Construct the full path to the file
            filepath = os.path.join(root_dir, filename)

            # Check if the file is a JSON file
            if filename.endswith('.json'):
                # Open the JSON file
                with open(filepath, 'r') as file:
                    # Load the JSON data
                    data = eval(file.read())

                    # Check if the JSON file contains the 'likes' key
                    if 'likes' in data:
                        # Check if the JSON file contains the 'liked_posts.json' key
                        if 'liked_posts.json' in data['likes']:
                            # Load the 'liked_posts.json' data
                            liked_posts_data = data['likes']['liked_posts.json']

                            # Check if the 'liked_posts.json' data contains the 'likes_media_likes' key
                            if 'likes_media_likes' in liked_posts_data:
                                # Iterate over each liked post
                                for post in liked_posts_data['likes_media_likes']:
                                    # Check if the post contains the 'string_list_data' key
                                    if 'string_list_data' in post:
                                        # Iterate over each string in the post
                                        for string in post['string_list_data']:
                                            # Check if the string contains the 'value' key
                                            if 'value' in string:
                                                # Extract the account information from the string
                                                account = string['value']

                                                # Add the account information to the list
                                                accounts.append(account)

        # Return the list of account information
        return accounts

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the data.")

def main():
    # Declare the variable referring to the file input
    root_dir = "root_dir"

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Get the account information
    accounts = get_account_info(root_dir)

    # Create a CSV writer
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Account'])

        # Write each account to the CSV file
        for account in accounts:
            writer.writerow([account])

if __name__ == "__main__":
    main()