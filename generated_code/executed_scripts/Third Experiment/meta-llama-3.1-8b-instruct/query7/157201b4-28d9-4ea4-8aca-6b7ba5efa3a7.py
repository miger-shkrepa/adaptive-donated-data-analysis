import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the engagement counts for each user
engagement_counts = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the necessary information
            if "connections" in data and "followers_and_following" in data["connections"] and "accounts_you've_favorited.json" in data["connections"]["followers_and_following"]:
                # Load the followers and following data
                followers_data = data["connections"]["followers_and_following"]["accounts_you've_favorited.json"]

                # Iterate over the relationships in the followers data
                for relationship in followers_data["structure"]["relationships_feed_favorites"]:
                    # Check if the relationship contains the necessary information
                    if "string_list_data" in relationship and "href" in relationship["string_list_data"][0] and "timestamp" in relationship["string_list_data"][0]:
                        # Extract the user and timestamp from the relationship
                        user = relationship["string_list_data"][0]["href"]
                        timestamp = relationship["string_list_data"][0]["timestamp"]

                        # Increment the engagement count for the user
                        if user in engagement_counts:
                            engagement_counts[user] += 1
                        else:
                            engagement_counts[user] = 1

# Initialize an empty list to store the results
results = []

# Iterate over the engagement counts
for user, count in engagement_counts.items():
    # Append the user and engagement count to the results list
    results.append([user, count])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])  # header
    writer.writerows(results)