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
    # Iterate over the files in the current directory
    for file_name in file_names:
        # Check if the file is a JSON file
        if file_name.endswith(".json"):
            # Construct the full path to the JSON file
            file_path = os.path.join(dir_path, file_name)
            try:
                # Open the JSON file and load its contents
                with open(file_path, 'r') as file:
                    data = file.read()
                    # Parse the JSON data
                    import json
                    parsed_data = json.loads(data)
                    # Check if the JSON data contains the required information
                    if "story_activities_story_likes" in parsed_data:
                        # Extract the user and engagement information
                        user = parsed_data["story_activities_story_likes"][0]["title"]
                        engagement = parsed_data["story_activities_story_likes"][0]["string_list_data"][0]["timestamp"]
                        # Update the user engagement dictionary
                        if user in user_engagement:
                            user_engagement[user] += engagement
                        else:
                            user_engagement[user] = engagement
            except Exception as e:
                # Handle any exceptions that occur while processing the JSON file
                print(f"Error processing {file_name}: {str(e)}")

# Sort the user engagement dictionary by engagement in descending order
sorted_user_engagement = dict(sorted(user_engagement.items(), key=lambda item: item[1], reverse=True))

# Write the user engagement data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['User', 'Times Engaged']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for user, engagement in sorted_user_engagement.items():
        writer.writerow({'User': user, 'Times Engaged': engagement})