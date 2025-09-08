import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize variables to store the results
account_views = {}
video_views = {}

# Function to process the ads information
def process_ads_info(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the data is in JSON format
            import json
            data = json.loads(data)
            for item in data['ads_and_topics']['ads_viewed.json']['structure']['impressions_history_ads_seen']:
                account = item['string_map_data']['Author']['value']
                if account in account_views:
                    account_views[account] += 1
                else:
                    account_views[account] = 1
            for item in data['ads_and_topics']['posts_viewed.json']['structure']['impressions_history_posts_seen']:
                account = item['string_map_data']['Author']['value']
                if account in account_views:
                    account_views[account] += 1
                else:
                    account_views[account] = 1
            for item in data['ads_and_topics']['videos_watched.json']['structure']['impressions_history_videos_watched']:
                account = item['string_map_data']['Author']['value']
                if account in video_views:
                    video_views[account] += 1
                else:
                    video_views[account] = 1
    except Exception as e:
        print(f"Error processing ads information: {e}")

# Function to process the instagram ads and businesses
def process_instagram_ads_info(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the data is in JSON format
            import json
            data = json.loads(data)
            for item in data['instagram_ads_and_businesses']['advertisers_using_your_activity_or_information.json']['structure']['ig_custom_audiences_all_types']:
                account = item['advertiser_name']
                if account in account_views:
                    account_views[account] += 1
                else:
                    account_views[account] = 1
    except Exception as e:
        print(f"Error processing instagram ads information: {e}")

# Function to process the other categories used to reach you
def process_other_categories_info(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Assuming the data is in JSON format
            import json
            data = json.loads(data)
            for item in data['instagram_ads_and_businesses']['other_categories_used_to_reach_you.json']['structure']['label_values']:
                account = item['ent_field_name']
                if account in account_views:
                    account_views[account] += 1
                else:
                    account_views[account] = 1
    except Exception as e:
        print(f"Error processing other categories information: {e}")

# Process the ads information
process_ads_info(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json'))
process_ads_info(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json'))
process_ads_info(os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json'))

# Process the instagram ads and businesses
process_instagram_ads_info(os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json'))

# Process the other categories used to reach you
process_other_categories_info(os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'other_categories_used_to_reach_you.json'))

# Create the result CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Account', 'Post Views', 'Video Views']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for account, views in account_views.items():
        writer.writerow({'Account': account, 'Post Views': views, 'Video Views': video_views.get(account, 0)})