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
type_list = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            
            # Check if the JSON data contains the required information
            if 'ads_information' in data and 'ads_and_topics' in data['ads_information']:
                # Iterate over the ads and topics
                for topic in data['ads_information']['ads_and_topics'].values():
                    # Check if the topic contains the required information
                    if 'structure' in topic and 'impressions_history_ads_seen' in topic['structure']:
                        # Iterate over the impressions history ads seen
                        for impression in topic['structure']['impressions_history_ads_seen']:
                            # Check if the impression contains the required information
                            if 'string_map_data' in impression and 'Time' in impression['string_map_data']:
                                # Extract the date and type
                                date = impression['string_map_data']['Time']['timestamp']
                                type = 'Daily'
                                
                                # Append the data to the lists
                                dates.append(date)
                                posts_viewed.append(1)
                                type_list.append(type)

# Create a dictionary to store the data
data_dict = {
    'Date/Week': dates,
    'Posts Viewed': posts_viewed,
    'Type': type_list
}

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.DictWriter(csvfile, fieldnames=['Date/Week', 'Posts Viewed', 'Type'])
    
    # Write the header
    writer.writeheader()
    
    # Write the data
    for i in range(len(dates)):
        # Check if the date is a week
        if dates[i] >= 7:
            # Format the date as a week
            dates[i] = f'Week {dates[i] // 7}-{dates[i] % 7 + 1}'
        
        # Write the data
        writer.writerow({
            'Date/Week': dates[i],
            'Posts Viewed': posts_viewed[i],
            'Type': type_list[i]
        })