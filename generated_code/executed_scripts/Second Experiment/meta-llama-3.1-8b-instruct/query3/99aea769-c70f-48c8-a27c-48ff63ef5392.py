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
                                # Get the date and posts viewed from the impression
                                date = impression['string_map_data']['Time']['timestamp']
                                posts_viewed = 1
                                
                                # Determine the type (daily or weekly)
                                if date % 7 == 0:
                                    type_list.append('Weekly')
                                else:
                                    type_list.append('Daily')
                                
                                # Add the date and posts viewed to the lists
                                dates.append(date)
                                posts_viewed.append(posts_viewed)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create the CSV writer
    writer = csv.writer(csvfile)
    
    # Write the column headers
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    
    # Write the data to the CSV file
    for i in range(len(dates)):
        writer.writerow([f'{dates[i]//10000}-{(dates[i]//100)%10}-{dates[i]%100}' if type_list[i] == 'Daily' else f'Week {dates[i]//10000}-{(dates[i]//100)%10}', posts_viewed[i], type_list[i]])

# Print a success message
print("Query executed successfully.")