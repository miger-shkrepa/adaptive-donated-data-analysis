import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
dates = []
posts_viewed = []
type = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            
            # Check if the JSON data has the required structure
            if 'ads_information' in data and 'ads_and_topics' in data['ads_information']:
                # Iterate over the ads and topics
                for topic in data['ads_information']['ads_and_topics'].values():
                    # Check if the topic has the required structure
                    if 'structure' in topic and 'impressions_history_ads_seen' in topic['structure']:
                        # Iterate over the impressions history ads seen
                        for impression in topic['structure']['impressions_history_ads_seen']:
                            # Check if the impression has the required structure
                            if 'string_map_data' in impression:
                                # Get the date and type from the impression
                                date = impression['string_map_data']['Time']['timestamp']
                                post_type = 'Daily'
                                
                                # Append the data to the lists
                                dates.append(date)
                                posts_viewed.append(1)
                                type.append(post_type)

# Create a dictionary to map the dates to weeks
date_to_week = {}
for date in dates:
    if date < 7:
        week = 'Week 2025-01'
    elif date < 14:
        week = 'Week 2025-02'
    else:
        week = 'Week 2025-03'
    date_to_week[date] = week

# Create a dictionary to store the weekly data
weekly_data = {}
for date, week in date_to_week.items():
    if week not in weekly_data:
        weekly_data[week] = 0
    weekly_data[week] += 1

# Append the weekly data to the lists
for week, count in weekly_data.items():
    dates.append(week)
    posts_viewed.append(count)
    type.append('Weekly')

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    
    # Write the data
    for date, post_viewed, post_type in zip(dates, posts_viewed, type):
        writer.writerow([date, post_viewed, post_type])