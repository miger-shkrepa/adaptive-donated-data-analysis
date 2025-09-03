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
posts_viewed_daily = []
posts_viewed_weekly = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            
            # Check if the file contains the required data
            if 'ads_and_topics' in data and 'ads_viewed.json' in data['ads_and_topics']:
                # Extract the data from the JSON file
                impressions_history_ads_seen = data['ads_and_topics']['ads_viewed.json']['structure']['impressions_history_ads_seen']
                
                # Iterate over the impressions history
                for impression in impressions_history_ads_seen:
                    # Extract the date and time from the impression
                    date = impression['string_map_data']['Time']['timestamp']
                    
                    # Convert the date to the required format
                    if date % 7 == 0:
                        date = f"Week {date // 7}-{date // 7 + 1}"
                    else:
                        date = f"{date // 1000000}-{(date // 10000) % 100}-{date % 10000}"
                    
                    # Add the date to the list
                    dates.append(date)
                    
                    # Increment the daily posts viewed count
                    posts_viewed_daily.append(1)
                    
                    # Increment the weekly posts viewed count
                    posts_viewed_weekly.append(1)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the column headers
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    
    # Write the data to the CSV file
    for i in range(len(dates)):
        writer.writerow([dates[i], posts_viewed_daily[i] + posts_viewed_weekly[i], 'Daily'])
        writer.writerow([dates[i], posts_viewed_weekly[i], 'Weekly'])