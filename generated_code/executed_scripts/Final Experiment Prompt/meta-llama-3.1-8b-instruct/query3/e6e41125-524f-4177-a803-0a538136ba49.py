import csv
import os
import json

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Set the input file path
input_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the input file exists
if not os.path.exists(input_file_path):
    print("Warning: Input file does not exist. Returning CSV file with only column headers.")
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    exit()

# Load the input file
try:
    with open(input_file_path, 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError("Error: Failed to parse JSON file: " + str(e))

# Initialize the output CSV file
output_file_path = 'query_responses/results.csv'
with open(output_file_path, 'w', newline='') as csvfile:
    fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Initialize daily and weekly counters
    daily_posts_viewed = 0
    weekly_posts_viewed = 0

    # Iterate over the impressions history
    for post in data['impressions_history_posts_seen']:
        timestamp = post['string_map_data']['Time']['timestamp']
        date = timestamp
        week = timestamp // 7 + 1  # Calculate the week number

        # Increment the daily or weekly counter
        if date == timestamp:
            daily_posts_viewed += 1
        else:
            weekly_posts_viewed += 1

        # Write the data to the output CSV file
        writer.writerow({
            'Date/Week': date if date == timestamp else f"Week {week}",
            'Posts Viewed': 1,
            'Type': 'Daily' if date == timestamp else 'Weekly'
        })

    # Write the total daily and weekly counts to the output CSV file
    writer.writerow({
        'Date/Week': 'Total',
        'Posts Viewed': daily_posts_viewed + weekly_posts_viewed,
        'Type': 'Daily'
    })
    writer.writerow({
        'Date/Week': 'Total',
        'Posts Viewed': weekly_posts_viewed,
        'Type': 'Weekly'
    })