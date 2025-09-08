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
    writer = csv.writer(csvfile)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

    # Iterate over the 'media' directory
    for date_dir in os.listdir(os.path.join(root_dir, 'media')):
        date_dir_path = os.path.join(root_dir, 'media', date_dir)
        if os.path.isdir(date_dir_path):
            # Initialize the daily and weekly counters
            daily_posts_viewed = 0
            weekly_posts_viewed = 0

            # Iterate over the files in the date directory
            for file in os.listdir(date_dir_path):
                file_path = os.path.join(date_dir_path, file)
                if os.path.isfile(file_path):
                    # Check if the file is a JSON file
                    if file.endswith('.json'):
                        try:
                            # Open the JSON file
                            with open(file_path, 'r') as json_file:
                                # Load the JSON data
                                data = json.load(json_file)

                                # Check if the JSON data has the expected structure
                                if 'ig_other_media' in data:
                                    # Iterate over the media items
                                    for media in data['ig_other_media']:
                                        # Increment the daily and weekly counters
                                        daily_posts_viewed += 1
                                        weekly_posts_viewed += 1

                                elif 'ig_reels_media' in data:
                                    # Iterate over the reels media items
                                    for media in data['ig_reels_media']:
                                        # Increment the daily and weekly counters
                                        daily_posts_viewed += 1
                                        weekly_posts_viewed += 1

                                elif 'ig_stories' in data:
                                    # Iterate over the stories items
                                    for story in data['ig_stories']:
                                        # Increment the daily and weekly counters
                                        daily_posts_viewed += 1
                                        weekly_posts_viewed += 1

                        except json.JSONDecodeError:
                            # If the JSON file is invalid, skip it
                            pass

            # Write the daily and weekly data to the CSV file
            if daily_posts_viewed > 0:
                writer.writerow([datetime.date.today().strftime('%Y-%m-%d'), daily_posts_viewed, 'Daily'])
            if weekly_posts_viewed > 0:
                writer.writerow([datetime.date.today().strftime('%Y-%W'), weekly_posts_viewed, 'Weekly'])