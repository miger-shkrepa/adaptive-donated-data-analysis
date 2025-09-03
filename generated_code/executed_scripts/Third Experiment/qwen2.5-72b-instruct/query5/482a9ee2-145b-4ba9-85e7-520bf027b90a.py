import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Device ID', 'Login Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Check if the necessary files exist
        if not os.path.exists(os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')):
            print("Warning: liked_posts.json does not exist. Treating its contribution as 0.")
        if not os.path.exists(os.path.join(root_dir, 'your_instagram_activity', 'saved', 'saved_posts.json')):
            print("Warning: saved_posts.json does not exist. Treating its contribution as 0.")

        # Since the provided structure does not contain login information, we can only write the headers.
        # If there were login data, we would parse the JSON files and extract the relevant information here.

except FileNotFoundError as e:
    print(e)
except Exception as e:
    raise ValueError(f"Error: An unexpected error occurred: {str(e)}")