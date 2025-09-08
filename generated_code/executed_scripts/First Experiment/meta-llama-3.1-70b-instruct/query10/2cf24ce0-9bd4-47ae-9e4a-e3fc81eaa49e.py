import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the account views
        account_views = {}

        # Iterate over the subdirectories in the root directory
        for subdir in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, subdir)

            # Check if the subdirectory is 'ads_information'
            if subdir == 'ads_information':
                # Iterate over the files in the 'ads_information' subdirectory
                for filename in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, filename)

                    # Check if the file is 'posts_viewed.json' or 'videos_watched.json'
                    if filename in ['posts_viewed.json', 'videos_watched.json']:
                        # Open the JSON file and load the data
                        with open(file_path, 'r') as file:
                            data = json.load(file)

                        # Iterate over the impressions history
                        for impression in data['impressions_history_posts_seen' if filename == 'posts_viewed.json' else 'impressions_history_videos_watched']:
                            # Get the author of the post or video
                            author = impression['string_map_data']['Author']['value']

                            # Increment the view count for the author
                            if author not in account_views:
                                account_views[author] = {'post_views': 0, 'video_views': 0}
                            if filename == 'posts_viewed.json':
                                account_views[author]['post_views'] += 1
                            else:
                                account_views[author]['video_views'] += 1

        return account_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_views):
    try:
        # Open the CSV file for writing
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Account', 'Post Views', 'Video Views'])

            # Write the account views to the CSV file
            for account, views in account_views.items():
                writer.writerow([account, views['post_views'], views['video_views']])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        account_views = get_account_views(root_dir)
        save_to_csv(account_views)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()