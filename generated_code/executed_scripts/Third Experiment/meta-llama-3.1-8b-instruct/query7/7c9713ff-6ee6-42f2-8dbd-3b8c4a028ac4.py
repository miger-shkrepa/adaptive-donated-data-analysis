import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the user and times engaged
users = []
times_engaged = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Check if the JSON data contains the required structure
            if "story_activities_questions" in data:
                # Extract the user and times engaged from the JSON data
                user = filename.split('.')[0]
                times_engaged.append(1)
                # Add the user and times engaged to the lists
                users.append(user)
            elif "story_activities_emoji_sliders" in data:
                # Extract the user and times engaged from the JSON data
                user = filename.split('.')[0]
                times_engaged.append(1)
                # Add the user and times engaged to the lists
                users.append(user)
            elif "story_activities_polls" in data:
                # Extract the user and times engaged from the JSON data
                user = filename.split('.')[0]
                times_engaged.append(1)
                # Add the user and times engaged to the lists
                users.append(user)
            elif "story_activities_emoji_quick_reactions" in data:
                # Extract the user and times engaged from the JSON data
                user = filename.split('.')[0]
                times_engaged.append(1)
                # Add the user and times engaged to the lists
                users.append(user)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create the CSV writer
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["User", "Times Engaged"])
    # Write the data to the CSV file
    for i in range(len(users)):
        writer.writerow([users[i], times_engaged[i]])