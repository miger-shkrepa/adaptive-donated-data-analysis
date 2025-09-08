import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Check if the JSON data contains the 'ads_information' key
            if 'ads_information' in data:
                # Check if the 'ads_information' key contains the 'ads_and_topics' key
                if 'ads_and_topics' in data:
                    # Check if the 'ads_and_topics' key contains the 'accounts_you\'re_not_interested_in.json' file
                    if 'accounts_you\'re_not_interested_in.json' in data:
                        # Extract the topics of interest from the JSON data
                        topics_of_interest.append('Accounts you\'re not interested in')
                    # Check if the 'ads_and_topics' key contains the 'ads_viewed.json' file
                    elif 'ads_viewed.json' in data:
                        # Extract the topics of interest from the JSON data
                        topics_of_interest.append('Ads viewed')
                    # Check if the 'ads_and_topics' key contains the 'posts_viewed.json' file
                    elif 'posts_viewed.json' in data:
                        # Extract the topics of interest from the JSON data
                        topics_of_interest.append('Posts viewed')
                    # Check if the 'ads_and_topics' key contains the 'suggested_accounts_viewed.json' file
                    elif 'suggested_accounts_viewed.json' in data:
                        # Extract the topics of interest from the JSON data
                        topics_of_interest.append('Suggested accounts viewed')
                    # Check if the 'ads_and_topics' key contains the 'videos_watched.json' file
                    elif 'videos_watched.json' in data:
                        # Extract the topics of interest from the JSON data
                        topics_of_interest.append('Videos watched')
            # Check if the JSON data contains the 'instagram_ads_and_businesses' key
            elif 'instagram_ads_and_businesses' in data:
                # Check if the 'instagram_ads_and_businesses' key contains the 'advertisers_using_your_activity_or_information.json' file
                if 'advertisers_using_your_activity_or_information.json' in data:
                    # Extract the topics of interest from the JSON data
                    topics_of_interest.append('Advertisers using your activity or information')

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Topics of Interest'])
    writer.writerows([[topic] for topic in topics_of_interest])