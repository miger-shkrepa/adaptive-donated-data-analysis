import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the user engagement counts
user_engagement_counts = {}

# Iterate over the 'stories' directory
for year in os.listdir(root_dir + "\\media\\stories"):
    for file in os.listdir(root_dir + "\\media\\stories\\" + year):
        # Check if the file is a JSON file
        if file.endswith(".json"):
            # Open the JSON file
            with open(root_dir + "\\media\\stories\\" + year + "\\" + file, 'r') as f:
                # Load the JSON data
                data = json.load(f)
                # Iterate over the 'profile_user' list
                for user in data['profile_user']:
                    # Get the user's username
                    username = user['string_map_data']['Username']['value']
                    # Get the user's engagement count
                    engagement_count = len(user['media_map_data'])
                    # Update the user engagement counts dictionary
                    if username in user_engagement_counts:
                        user_engagement_counts[username] += engagement_count
                    else:
                        user_engagement_counts[username] = engagement_count

# Sort the user engagement counts in descending order
sorted_user_engagement_counts = dict(sorted(user_engagement_counts.items(), key=lambda item: item[1], reverse=True))

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['User', 'Times Engaged'])
    # Write the user engagement counts
    for user, engagement_count in sorted_user_engagement_counts.items():
        writer.writerow([user, engagement_count])