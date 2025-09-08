import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
date_week_list = []
posts_viewed_list = []
type_list = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if 'ads_information' in data and 'ads_and_topics' in data['ads_information']:
                # Iterate over the ads and topics
                for topic in data['ads_information']['ads_and_topics'].values():
                    # Check if the topic contains the required information
                    if 'posts_viewed.json' in topic and 'structure' in topic['posts_viewed.json']:
                        # Iterate over the posts viewed
                        for post in topic['posts_viewed.json']['structure']['impressions_history_posts_seen']:
                            # Check if the post contains the required information
                            if 'string_map_data' in post and 'Time' in post['string_map_data']:
                                # Get the date and week from the timestamp
                                timestamp = post['string_map_data']['Time']['timestamp']
                                date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                                week = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%W')

                                # Add the data to the lists
                                date_week_list.append(date)
                                posts_viewed_list.append(1)
                                type_list.append('Daily')

                                # Add the data to the lists for the week
                                date_week_list.append(week)
                                posts_viewed_list.append(1)
                                type_list.append('Weekly')

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    for i in range(len(date_week_list)):
        writer.writerow([date_week_list[i], posts_viewed_list[i], type_list[i]])