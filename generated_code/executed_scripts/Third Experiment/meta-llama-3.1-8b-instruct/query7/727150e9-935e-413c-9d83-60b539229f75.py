import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the user engagement data
user_engagement = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains user engagement information
            if "relationships_follow_requests_received" in data["json"]["structure"]:
                # Iterate over the user engagement data
                for user in data["json"]["structure"]["relationships_follow_requests_received"]:
                    # Check if the user is already in the dictionary
                    if user["title"] in user_engagement:
                        # Increment the user's engagement count
                        user_engagement[user["title"]] += 1
                    else:
                        # Add the user to the dictionary with an engagement count of 1
                        user_engagement[user["title"]] = 1

# Initialize an empty list to store the user engagement data
engagement_data = []

# Iterate over the user engagement data
for user, engagement in user_engagement.items():
    # Append the user engagement data to the list
    engagement_data.append([user, engagement])

# Write the user engagement data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["User", "Times Engaged"])
    # Write the user engagement data
    writer.writerows(engagement_data)