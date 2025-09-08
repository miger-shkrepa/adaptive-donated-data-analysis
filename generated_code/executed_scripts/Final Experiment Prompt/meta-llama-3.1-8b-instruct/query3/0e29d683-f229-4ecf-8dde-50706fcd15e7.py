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
                date = post['string_map_data']['Time']['timestamp']

                # Determine the type (daily or weekly)
                if date < 7 * 24 * 60 * 60:  # 7 days
                    type = 'Daily'
                else:
                    type = 'Weekly'

                # Increment the counter
                if type == 'Daily':
                    daily_posts_viewed += 1
                else:
                    weekly_posts_viewed += 1

                # Write the row to the output CSV file
                writer.writerow([date, daily_posts_viewed + weekly_posts_viewed, type])

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON in input file.")
    except Exception as e:
        raise Exception("Error: An unexpected error occurred.")