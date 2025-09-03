import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = []

# Iterate over the 'your_instagram_activity' directory
for filename in os.listdir(os.path.join(root_dir, "your_instagram_activity")):
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, "your_instagram_activity", filename), "r") as f:
            data = json.load(f)

            # Check if the file contains the required data
            if "story_activities_story_likes" in data["structure"]:
                # Extract the user and times engaged
                user = data["structure"]["story_activities_story_likes"][0]["title"]
                times_engaged = len(data["structure"]["story_activities_story_likes"][0]["string_list_data"])

                # Append the result to the list
                results.append((user, times_engaged))

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    writer.writerows(results)