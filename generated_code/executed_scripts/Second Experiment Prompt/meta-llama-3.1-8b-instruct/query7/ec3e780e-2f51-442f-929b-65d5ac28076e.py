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
                    json_data = json.loads(data)
                    # Check if the JSON data contains the required information
                    if "story_activities_story_likes" in json_data:
                        # Extract the user ID and engagement time from the JSON data
                        user_id = json_data["story_activities_story_likes"][0]["title"]
                        engagement_time = json_data["story_activities_story_likes"][0]["string_list_data"][0]["timestamp"]
                        # Update the user engagement dictionary
                        if user_id in user_engagement:
                            user_engagement[user_id].append(engagement_time)
                        else:
                            user_engagement[user_id] = [engagement_time]
            except Exception as e:
                # Handle any exceptions that occur while processing the JSON file
                print(f"Error processing file {file_path}: {str(e)}")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["User", "Times Engaged"])
    # Iterate over the user engagement dictionary
    for user_id, engagement_times in user_engagement.items():
        # Calculate the total engagement time for the user
        total_engagement_time = sum(engagement_times)
        # Write the user engagement data to the CSV file
        writer.writerow([user_id, len(engagement_times)])