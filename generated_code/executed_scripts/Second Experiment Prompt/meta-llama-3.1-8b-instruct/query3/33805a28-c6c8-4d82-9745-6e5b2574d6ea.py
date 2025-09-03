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

    # Iterate over the 'ads_information' directory
    for filename in os.listdir(os.path.join(root_dir, 'ads_information', 'ads_and_topics')):
        if filename.endswith('.json'):
            filepath = os.path.join(root_dir, 'ads_information', 'ads_and_topics', filename)
            try:
                with open(filepath, 'r') as file:
                    data = json.load(file)

                    # Extract the 'impressions_history_ads_seen' list
                    impressions_history_ads_seen = data.get('structure', {}).get('impressions_history_ads_seen', [])

                    # Initialize the daily and weekly counters
                    daily_posts_viewed = 0
                    weekly_posts_viewed = 0

                    # Iterate over the 'impressions_history_ads_seen' list
                    for item in impressions_history_ads_seen:
                        string_map_data = item.get('string_map_data', {})

                        # Extract the 'Author' and 'Time' values
                        author = string_map_data.get('Author', {}).get('value')
                        time = string_map_data.get('Time', {}).get('timestamp')

                        # Skip if either 'Author' or 'Time' is missing
                        if author is None or time is None:
                            continue

                        # Convert the time to a datetime object
                        dt = datetime.datetime.fromtimestamp(time)

                        # Determine the date or week
                        if dt.date() == dt.date():
                            # Daily
                            daily_posts_viewed += 1
                        else:
                            # Weekly
                            weekly_posts_viewed += 1

                    # Write the results to the CSV file
                    if daily_posts_viewed > 0 or weekly_posts_viewed > 0:
                        writer.writerow([dt.strftime('%Y-%m-%d'), daily_posts_viewed, 'Daily'])
                        writer.writerow([dt.strftime('%Y-%W'), weekly_posts_viewed, 'Weekly'])
            except FileNotFoundError:
                # If the file does not exist, treat its contribution as 0
                pass
            except json.JSONDecodeError:
                # If the file is not a valid JSON, treat its contribution as 0
                pass