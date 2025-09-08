import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the user and times engaged dictionaries
user_engagement = {}

# Iterate over the 'stories' directory
for dir_name, dir_contents, _ in os.walk(os.path.join(root_dir, "media", "stories")):
    # Iterate over the JSON files in the directory
    for file_name in dir_contents:
        if file_name.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(dir_name, file_name), "r") as file:
                # Load the JSON data
                data = eval(file.read())

                # Extract the user ID from the file name
                user_id = file_name.split(".")[0]

                # Initialize the engagement count for the user
                user_engagement[user_id] = 0

                # Iterate over the story interactions
                for story in data["ig_stories"]:
                    # Increment the engagement count for the user
                    user_engagement[user_id] += 1

# Create the CSV file
with open("query_responses/results.csv", "w", newline="") as file:
    # Create the CSV writer
    writer = csv.writer(file)

    # Write the column headers
    writer.writerow(["User", "Times Engaged"])

    # Write the user engagement data
    for user, engagement in user_engagement.items():
        writer.writerow([user, engagement])