import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the accounts
accounts = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if 'ads_information' in data and 'ads_and_topics' in data['ads_information'] and 'posts_viewed.json' in data['ads_information']['ads_and_topics']:
                # Open the posts_viewed.json file
                with open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json'), 'r') as posts_file:
                    # Load the posts_viewed.json data
                    posts_data = eval(posts_file.read())

                    # Check if the posts_viewed.json data contains the required information
                    if 'impressions_history_posts_seen' in posts_data['structure']:
                        # Iterate over the impressions_history_posts_seen data
                        for post in posts_data['structure']['impressions_history_posts_seen']:
                            # Check if the post contains the required information
                            if 'string_map_data' in post and 'Author' in post['string_map_data'] and 'Time' in post['string_map_data']:
                                # Extract the author and time from the post
                                author = post['string_map_data']['Author']['value']
                                time = post['string_map_data']['Time']['timestamp']

                                # Check if the author is not in the accounts list
                                if author not in accounts:
                                    # Add the author to the accounts list
                                    accounts.append(author)

            # Check if the JSON data contains the required information
            if 'connections' in data and 'followers_and_following' in data['connections'] and 'accounts_you\'ve_favorited.json' in data['connections']['followers_and_following']:
                # Open the accounts_you've_favorited.json file
                with open(os.path.join(root_dir, 'connections', 'followers_and_following', 'accounts_you\'ve_favorited.json'), 'r') as favorites_file:
                    # Load the accounts_you've_favorited.json data
                    favorites_data = eval(favorites_file.read())

                    # Check if the accounts_you've_favorited.json data contains the required information
                    if 'relationships_feed_favorites' in favorites_data['structure']:
                        # Iterate over the relationships_feed_favorites data
                        for favorite in favorites_data['structure']['relationships_feed_favorites']:
                            # Check if the favorite contains the required information
                            if 'string_list_data' in favorite and len(favorite['string_list_data']) > 0:
                                # Extract the favorite from the favorite
                                favorite = favorite['string_list_data'][0]['value']

                                # Check if the favorite is in the accounts list
                                if favorite in accounts:
                                    # Remove the favorite from the accounts list
                                    accounts.remove(favorite)

# Write the accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account'])
    writer.writerows([[account] for account in accounts])