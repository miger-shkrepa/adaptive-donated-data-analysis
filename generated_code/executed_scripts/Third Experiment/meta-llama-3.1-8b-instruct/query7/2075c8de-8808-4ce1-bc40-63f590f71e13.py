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

# Iterate over the story interactions
for file in os.listdir(root_dir):
    if file.endswith(".json"):
        with open(os.path.join(root_dir, file), 'r') as f:
            data = eval(f.read())
            for story in data['story_interactions'][file.split('.')[0]].get('story_activities_story_likes', []):
                for item in story.get('string_list_data', []):
                    users.append(item.get('value', ''))
                    times_engaged.append(item.get('timestamp', 0))

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for i in range(len(users)):
        writer.writerow([users[i], times_engaged[i]])

print("The script has finished running.")