import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize a dictionary to store the results
results = {
    'Account': [],
    'Post Views': [],
    'Video Views': []
}

# Function to process the directory and extract the required data
def process_directory(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize counters for post views and video views
        post_views = 0
        video_views = 0

        # Walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                        # Check for post views
                        if 'likes_media_likes' in data:
                            post_views += len(data['likes_media_likes'])

                        # Check for video views
                        if 'likes_comment_likes' in data:
                            video_views += len(data['likes_comment_likes'])

        # Add the results to the dictionary
        results['Account'].append('User')
        results['Post Views'].append(post_views)
        results['Video Views'].append(video_views)

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Function to write the results to a CSV file
def write_to_csv(results, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(results.keys())
            writer.writerows(zip(*results.values()))
    except Exception as e:
        print(f"Error: {e}")

# Process the directory and write the results to the CSV file
process_directory(root_dir)
write_to_csv(results, output_csv)