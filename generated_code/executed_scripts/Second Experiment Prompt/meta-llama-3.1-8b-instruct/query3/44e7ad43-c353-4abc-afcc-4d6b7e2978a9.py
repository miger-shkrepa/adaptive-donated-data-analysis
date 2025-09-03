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
    fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Initialize the total posts viewed
    total_posts_viewed = 0

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'posts_viewed.json':
                # Open the JSON file
                try:
                    with open(os.path.join(dirpath, filename), 'r') as json_file:
                        data = json.load(json_file)

                        # Check if the 'structure' key exists
                        if 'structure' in data:
                            # Extract the data
                            posts_viewed = data['structure']['impressions_history_posts_seen']

                            # Iterate over the posts viewed
                            for post in posts_viewed:
                                # Extract the date and time
                                date = post['string_map_data']['Time']['timestamp']

                                # Convert the date to a datetime object
                                dt = datetime.datetime.fromtimestamp(date)

                                # Determine the type (daily or weekly)
                                if dt.date() == dt.date():
                                    type = 'Daily'
                                else:
                                    type = 'Weekly'

                                # Write the data to the CSV file
                                writer.writerow({
                                    'Date/Week': dt.strftime('%Y-%m-%d') if type == 'Daily' else f'Week {dt.strftime("%Y-%W")}',
                                    'Posts Viewed': 1,
                                    'Type': type
                                })

                                # Increment the total posts viewed
                                total_posts_viewed += 1
                        else:
                            # If the 'structure' key does not exist, treat its contribution as 0
                            print(f"Warning: File '{os.path.join(dirpath, filename)}' does not contain the 'structure' key. Skipping...")
                except FileNotFoundError:
                    # If the file does not exist, treat its contribution as 0
                    print(f"Error: File '{os.path.join(dirpath, filename)}' does not exist.")
                except json.JSONDecodeError:
                    # If the JSON file is malformed, treat its contribution as 0
                    print(f"Error: Malformed JSON file '{os.path.join(dirpath, filename)}'.")

    # Write the total posts viewed to the CSV file
    writer.writerow({
        'Date/Week': 'Total',
        'Posts Viewed': total_posts_viewed,
        'Type': 'Total'
    })