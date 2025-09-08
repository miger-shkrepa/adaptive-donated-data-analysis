import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Iterate over the directory structure
for filename in os.listdir(root_dir):
    if filename.endswith('.json'):
        try:
            with open(os.path.join(root_dir, filename)) as file:
                data = json.load(file)
                if 'ads_and_topics' in data and 'ads_viewed.json' in data['ads_and_topics']:
                    ads_viewed = data['ads_and_topics']['ads_viewed.json']
                    if 'impressions_history_posts_seen' in ads_viewed['structure']:
                        posts_viewed = ads_viewed['structure']['impressions_history_posts_seen']
                        if 'likes_media_likes' in data['ads_and_topics']:
                            likes = data['ads_and_topics']['likes_media_likes']
                            for post in posts_viewed:
                                for like in likes:
                                    if post['string_map_data']['Author']['value'] == like['string_list_data'][0]['value']:
                                        results.append([post['string_map_data']['Author']['value']])
                                        break
        except FileNotFoundError:
            pass

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account'])
    for result in results:
        writer.writerow(result)