import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = 'query_responses/results.csv'

# Initialize the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])

    # Initialize a dictionary to store the engagement count for each user
    engagement_counts = {}

    # Iterate over the stories directory
    stories_dir = os.path.join(root_dir, "media", "stories")
    if os.path.exists(stories_dir):
        for year_dir in os.listdir(stories_dir):
            year_dir_path = os.path.join(stories_dir, year_dir)
            if os.path.isdir(year_dir_path):
                for user_file in os.listdir(year_dir_path):
                    user_file_path = os.path.join(year_dir_path, user_file)
                    if user_file.endswith(".json"):
                        try:
                            with open(user_file_path, 'r') as json_file:
                                user_data = json.load(json_file)
                                # Check if the user has engagement data
                                if "ig_stories" in user_data:
                                    # Initialize the engagement count for the user
                                    engagement_count = 0

                                    # Iterate over the engagement data
                                    for engagement in user_data["ig_stories"]:
                                        # Increment the engagement count
                                        engagement_count += 1

                                    # Store the engagement count in the dictionary
                                    engagement_counts[user_file.split(".")[0]] = engagement_count
                        except json.JSONDecodeError:
                            # If the file is not a valid JSON, skip it
                            pass
    else:
        # If the stories directory does not exist, write the column headers to the CSV file
        writer.writerow(["User", "Times Engaged"])

    # Find the user with the most engagement
    if engagement_counts:
        max_engagement = max(engagement_counts.values())
        users_with_max_engagement = [user for user, count in engagement_counts.items() if count == max_engagement]

        # Write the users with the most engagement to the CSV file
        for user in users_with_max_engagement:
            writer.writerow([user, max_engagement])
    else:
        # If no engagement data is found, write the column headers to the CSV file
        writer.writerow(["User", "Times Engaged"])