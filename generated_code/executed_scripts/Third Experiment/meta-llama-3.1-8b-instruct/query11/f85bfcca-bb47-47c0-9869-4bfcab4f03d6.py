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

            # Check if the JSON data contains the necessary information
            if 'ads_information' in data and 'ads_and_topics' in data['ads_information'] and 'posts_viewed.json' in data['ads_information']['ads_and_topics']:
                # Load the posts viewed data
                posts_viewed_data = data['ads_information']['ads_and_topics']['posts_viewed.json']

                # Check if the posts viewed data contains the necessary information
                if 'impressions_history_posts_seen' in posts_viewed_data['structure']:
                    # Load the impressions history posts seen data
                    impressions_history_posts_seen_data = posts_viewed_data['structure']['impressions_history_posts_seen']

                    # Check if the impressions history posts seen data contains the necessary information
                    if impressions_history_posts_seen_data:
                        # Iterate over the impressions history posts seen data
                        for post in impressions_history_posts_seen_data:
                            # Check if the post contains the necessary information
                            if 'string_map_data' in post and 'Author' in post['string_map_data']:
                                # Get the author of the post
                                author = post['string_map_data']['Author']['value']

                                # Check if the author is not in the accounts list
                                if author not in accounts:
                                    # Add the author to the accounts list
                                    accounts.append(author)

            # Check if the JSON data contains the necessary information
            if 'connections' in data and 'followers_and_following' in data['connections'] and 'following.json' in data['connections']['followers_and_following']:
                # Load the following data
                following_data = data['connections']['followers_and_following']['following.json']

                # Check if the following data contains the necessary information
                if 'structure' in following_data and 'relationships_following' in following_data['structure']:
                    # Load the relationships following data
                    relationships_following_data = following_data['structure']['relationships_following']

                    # Check if the relationships following data contains the necessary information
                    if relationships_following_data:
                        # Iterate over the relationships following data
                        for relationship in relationships_following_data:
                            # Check if the relationship contains the necessary information
                            if 'string_list_data' in relationship and 'href' in relationship['string_list_data'][0]:
                                # Get the href of the relationship
                                href = relationship['string_list_data'][0]['href']

                                # Check if the href is not in the accounts list
                                if href not in accounts:
                                    # Add the href to the accounts list
                                    accounts.append(href)

# Write the accounts to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account'])
    writer.writerows([[account] for account in accounts])