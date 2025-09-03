import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
date_week = []
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
            
            # Check if the JSON data contains the required information
            if 'ads_viewed.json' in filename:
                # Iterate over the impressions history ads seen
                for impression in data['structure']['impressions_history_ads_seen']:
                    # Extract the date and time
                    date = impression['string_map_data']['Time']['timestamp']
                    # Convert the date to the required format
                    if date % 7 == 0:
                        date_week.append(f"Week {date // 7}-{date // 7 + 1}")
                        type.append('Weekly')
                    else:
                        date_week.append(f"2025-{date // 7 + 1:02d}")
                        type.append('Daily')
                    # Increment the posts viewed count
                    posts_viewed.append(1)
            elif 'posts_viewed.json' in filename:
                # Iterate over the impressions history posts seen
                for impression in data['structure']['impressions_history_posts_seen']:
                    # Extract the date and time
                    date = impression['string_map_data']['Time']['timestamp']
                    # Convert the date to the required format
                    if date % 7 == 0:
                        date_week.append(f"Week {date // 7}-{date // 7 + 1}")
                        type.append('Weekly')
                    else:
                        date_week.append(f"2025-{date // 7 + 1:02d}")
                        type.append('Daily')
                    # Increment the posts viewed count
                    posts_viewed.append(1)
            elif 'videos_watched.json' in filename:
                # Iterate over the impressions history videos watched
                for impression in data['structure']['impressions_history_videos_watched']:
                    # Extract the date and time
                    date = impression['string_map_data']['Time']['timestamp']
                    # Convert the date to the required format
                    if date % 7 == 0:
                        date_week.append(f"Week {date // 7}-{date // 7 + 1}")
                        type.append('Weekly')
                    else:
                        date_week.append(f"2025-{date // 7 + 1:02d}")
                        type.append('Daily')
                    # Increment the posts viewed count
                    posts_viewed.append(1)

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    for i in range(len(date_week)):
        writer.writerow([date_week[i], posts_viewed[i], type[i]])