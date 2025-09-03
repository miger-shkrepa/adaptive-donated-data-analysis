import csv
import os
import datetime
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'posts_viewed.json':
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as file:
                        data = file.read()
                        # Parse the JSON data
                        data = json.loads(data)
                        # Check if the structure key exists
                        if 'structure' in data:
                            # Extract the impressions history posts seen
                            impressions_history_posts_seen = data['structure']['impressions_history_posts_seen']
                            # Iterate over the impressions history posts seen
                            for post in impressions_history_posts_seen:
                                # Extract the string map data
                                string_map_data = post.get('string_map_data', {})
                                # Extract the time
                                time = string_map_data.get('Time', {}).get('value')
                                # Convert the time to a datetime object
                                if time is not None:
                                    dt = datetime.datetime.fromtimestamp(int(time))
                                    # Format the datetime object as a string
                                    date_str = dt.strftime('%Y-%m-%d')
                                    # Determine the type (daily or weekly)
                                    if dt.weekday() == 0:  # Monday
                                        type_str = 'Weekly'
                                    else:
                                        type_str = 'Daily'
                                    # Write the data to the CSV file
                                    writer.writerow([date_str, len(impressions_history_posts_seen), type_str])
                        else:
                            # If the structure key does not exist, treat its contribution as 0
                            writer.writerow(['', 0, ''])
                except FileNotFoundError:
                    # If the file does not exist, treat its contribution as 0
                    writer.writerow(['', 0, ''])
                except ValueError:
                    # If the JSON data is invalid, treat its contribution as 0
                    writer.writerow(['', 0, ''])