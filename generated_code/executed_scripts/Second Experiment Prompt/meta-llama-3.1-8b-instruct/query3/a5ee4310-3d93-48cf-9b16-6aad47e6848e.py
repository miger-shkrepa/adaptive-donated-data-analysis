import csv
import os
import datetime

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

    # Iterate over the files in the root directory
    for filename in os.listdir(root_dir):
        # Check if the file is a JSON file
        if filename.endswith('.json'):
            # Open the JSON file
            with open(os.path.join(root_dir, filename), 'r') as json_file:
                # Load the JSON data
                data = json.load(json_file)

                # Check if the file contains the required data
                if 'ads_information' in data and 'ads_and_topics' in data['ads_information'] and 'ads_viewed.json' in data['ads_information']['ads_and_topics']:
                    # Load the ads_viewed.json data
                    ads_viewed_data = data['ads_information']['ads_and_topics']['ads_viewed.json']

                    # Extract the impressions_history_ads_seen data
                    impressions_history_ads_seen = ads_viewed_data['structure']['impressions_history_ads_seen']

                    # Initialize the daily and weekly counts
                    daily_count = 0
                    weekly_count = 0

                    # Iterate over the impressions_history_ads_seen data
                    for impression in impressions_history_ads_seen:
                        # Extract the string_map_data
                        string_map_data = impression['string_map_data']

                        # Check if the string_map_data contains the required data
                        if 'Author' in string_map_data and 'Time' in string_map_data:
                            # Increment the daily count
                            daily_count += 1

                            # Get the date from the Time field
                            date = datetime.datetime.fromtimestamp(string_map_data['Time']['timestamp'])

                            # Check if the date is a weekday
                            if date.weekday() < 5:
                                # Increment the weekly count
                                weekly_count += 1

                    # Write the data to the CSV file
                    writer.writerow({
                        'Date/Week': date.strftime('%Y-%m-%d') if date.weekday() < 5 else f'Week {date.strftime("%Y-%W")}',
                        'Posts Viewed': daily_count,
                        'Type': 'Daily' if date.weekday() < 5 else 'Weekly'
                    })

                # If the file does not contain the required data, treat its contribution as 0
                else:
                    writer.writerow({
                        'Date/Week': '',
                        'Posts Viewed': 0,
                        'Type': ''
                    })