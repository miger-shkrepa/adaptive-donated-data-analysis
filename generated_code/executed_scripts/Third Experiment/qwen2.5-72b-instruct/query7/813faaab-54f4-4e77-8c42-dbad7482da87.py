import os
import json
import csv

root_dir = "root_dir"

def process_stories_engagement(root_dir):
    user_engagement = {}
    stories_path = os.path.join(root_dir, "stories")

    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    if not os.path.exists(stories_path):
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
        return

    for year_month in os.listdir(stories_path):
        year_month_path = os.path.join(stories_path, year_month)
        if os.path.isdir(year_month_path):
            for file in os.listdir(year_month_path):
                file_path = os.path.join(year_month_path, file)
                if file.endswith('.mp4') or file.endswith('.jpg'):
                    try:
                        # Since the files are not JSON, we cannot extract user engagement data directly.
                        # We treat the presence of a file as an engagement event.
                        user = file.split('_')[0]  # Assuming the user ID is the first part of the filename
                        if user in user_engagement:
                            user_engagement[user] += 1
                        else:
                            user_engagement[user] = 1
                    except Exception as e:
                        raise ValueError(f"Error: Failed to process file {file}. Reason: {str(e)}")

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
        for user, count in user_engagement.items():
            writer.writerow([user, count])

try:
    process_stories_engagement(root_dir)
except Exception as e:
    print(str(e))