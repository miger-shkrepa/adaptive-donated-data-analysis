import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize variables to store the results
user_engagement = {}

# Iterate over the 'connections' directory
for user in os.listdir(os.path.join(root_dir, "connections", "followers_and_following")):
    # Check if the user has a 'close_friends.json' file
    close_friends_file = os.path.join(root_dir, "connections", "followers_and_following", user, "close_friends.json")
    if os.path.exists(close_friends_file):
        # Open the 'close_friends.json' file
        with open(close_friends_file, 'r') as file:
            # Load the JSON data
            data = file.read()
            # Parse the JSON data
            import json
            close_friends_data = json.loads(data)
            # Iterate over the 'close_friends' list
            for friend in close_friends_data['relationships_close_friends']:
                # Get the user's name
                user_name = friend['title']
                # Get the number of times the user engaged with the friend's story
                engagement_count = len(friend['string_list_data'])
                # Store the engagement count in the user_engagement dictionary
                if user_name in user_engagement:
                    user_engagement[user_name] += engagement_count
                else:
                    user_engagement[user_name] = engagement_count

# Sort the user_engagement dictionary by value in descending order
sorted_user_engagement = dict(sorted(user_engagement.items(), key=lambda item: item[1], reverse=True))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['User', 'Times Engaged'])
    # Write the results
    for user, engagement_count in sorted_user_engagement.items():
        writer.writerow([user, engagement_count])