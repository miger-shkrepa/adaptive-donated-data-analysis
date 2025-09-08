import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize the CSV writer
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the column headers
        writer.writeheader()

        # Initialize the counters for post and video views
        post_views = 0
        video_views = 0

        # Iterate over the JSON files in the 'ads_and_topics' directory
        for file in os.listdir(os.path.join(root_dir, 'ads_and_topics')):
            if file.endswith('.json'):
                with open(os.path.join(root_dir, 'ads_and_topics', file), 'r') as json_file:
                    data = json.load(json_file)

                    # Check if the file contains the necessary data
                    if 'impressions_history_ads_seen' in data['structure']:
                        for impression in data['structure']['impressions_history_ads_seen']:
                            if 'string_map_data' in impression:
                                if 'Author' in impression['string_map_data']:
                                    post_views += 1
                                if 'string_map_data' in impression and 'Time' in impression['string_map_data']:
                                    video_views += 1

        # Write the results to the CSV file
        writer.writerow({'Account': 'Total', 'Post Views': post_views, 'Video Views': video_views})

except FileNotFoundError as e:
    print(e)
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

except Exception as e:
    print(e)