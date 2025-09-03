import os
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate over media directories
        media_dir = os.path.join(root_dir, "media")
        if os.path.exists(media_dir):
            for media_type in os.listdir(media_dir):
                media_type_dir = os.path.join(media_dir, media_type)
                if os.path.isdir(media_type_dir):
                    for date_dir in os.listdir(media_type_dir):
                        date_dir_path = os.path.join(media_type_dir, date_dir)
                        if os.path.isdir(date_dir_path):
                            for file in os.listdir(date_dir_path):
                                file_path = os.path.join(date_dir_path, file)
                                if os.path.isfile(file_path):
                                    # Assuming file name contains account information
                                    account = file.split('.')[0]
                                    if account not in account_views:
                                        account_views[account] = {'Post Views': 0, 'Video Views': 0}
                                    if media_type in ['posts', 'stories']:
                                        account_views[account]['Post Views'] += 1
                                    elif media_type in ['reels']:
                                        account_views[account]['Video Views'] += 1

        # Write results to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account, views in account_views.items():
                writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except Exception as e:
        raise ValueError(f"Error: {e}")

get_account_views(root_dir)