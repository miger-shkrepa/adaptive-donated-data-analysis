import csv
import json
import os

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Set the input file path
input_file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

# Check if the input file exists
if not os.path.exists(input_file_path):
    print("Warning: Input file does not exist. Returning CSV file with only column headers.")
else:
    try:
        # Load the input file
        with open(input_file_path, 'r') as input_file:
            input_data = json.load(input_file)

        # Initialize the output CSV file
        output_file_path = 'query_responses/results.csv'
        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)

            # Write the column headers
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

            # Initialize the daily and weekly counters
            daily_posts_viewed = 0
            weekly_posts_viewed = 0

            # Iterate over the impressions history
            for post in input_data['impressions_history_posts_seen']:
                timestamp = post['string_map_data']['Time']['timestamp']

                # Determine the date or week
                date = timestamp
                if isinstance(timestamp, int):
                    # If timestamp is an integer, it's a daily count
                    daily_posts_viewed += 1
                    week = None
                else:
                    # If timestamp is not an integer, it's a weekly count
                    weekly_posts_viewed += 1
                    week = timestamp.strftime('%Y-%W')

                # Write the data to the output CSV file
                if week is None:
                    writer.writerow([date, daily_posts_viewed, 'Daily'])
                else:
                    writer.writerow([week, weekly_posts_viewed, 'Weekly'])

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON file: " + str(e))
    except Exception as e:
        raise Exception("Error: An unexpected error occurred: " + str(e))