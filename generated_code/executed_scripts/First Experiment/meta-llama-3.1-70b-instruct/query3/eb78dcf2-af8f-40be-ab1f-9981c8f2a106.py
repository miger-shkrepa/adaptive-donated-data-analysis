import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_post_views(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store post views
        post_views = {}

        # Iterate over the files in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename), 'r') as file:
                    # Load the JSON data
                    data = json.load(file)

                    # Check if the file contains post data
                    if 'story_activities' in data:
                        # Iterate over the post data
                        for post in data['story_activities']:
                            # Get the timestamp of the post
                            timestamp = post['timestamp']

                            # Convert the timestamp to a datetime object
                            date = datetime.fromtimestamp(timestamp)

                            # Get the date and week of the post
                            date_str = date.strftime('%Y-%m-%d')
                            week_str = f"Week {date.strftime('%Y-%U')}"

                            # Increment the post views for the date and week
                            if date_str not in post_views:
                                post_views[date_str] = {'Daily': 0, 'Weekly': 0}
                            if week_str not in post_views:
                                post_views[week_str] = {'Daily': 0, 'Weekly': 0}

                            post_views[date_str]['Daily'] += 1
                            post_views[week_str]['Weekly'] += 1

        return post_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(post_views):
    try:
        # Open the CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)

            # Write the header
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

            # Write the post views to the CSV file
            for date, views in post_views.items():
                if 'Daily' in views:
                    writer.writerow([date, views['Daily'], 'Daily'])
                if 'Weekly' in views:
                    writer.writerow([date, views['Weekly'], 'Weekly'])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        post_views = get_post_views(root_dir)
        save_to_csv(post_views)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()