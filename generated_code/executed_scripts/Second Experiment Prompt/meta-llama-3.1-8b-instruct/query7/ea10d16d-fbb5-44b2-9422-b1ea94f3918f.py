import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the user engagement dictionary
user_engagement = {}

# Iterate over the directory structure
for dir_path, dir_names, file_names in os.walk(root_dir):
    for file_name in file_names:
        # Check if the file is a JSON file
        if file_name.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(dir_path, file_name), "r") as file:
                # Load the JSON data
                try:
                    data = eval(file.read())
                except Exception as e:
                    print(f"Error parsing JSON file {file_name}: {e}")
                    continue

                # Check if the JSON data contains the required information
                if "story_activities_story_likes" in data:
                    # Iterate over the story likes
                    for story_like in data.get("story_activities_story_likes", []):
                        # Get the user who posted the story
                        user = story_like.get("title", "")

                        # Increment the user engagement count
                        if user:
                            if user in user_engagement:
                                user_engagement[user] += 1
                            else:
                                user_engagement[user] = 1

# Create the CSV file
with open("query_responses/results.csv", "w", newline="") as csv_file:
    # Create the CSV writer
    writer = csv.writer(csv_file)

    # Write the column headers
    writer.writerow(["User", "Times Engaged"])

    # Write the user engagement data
    for user, engagement in user_engagement.items():
        writer.writerow([user, engagement])