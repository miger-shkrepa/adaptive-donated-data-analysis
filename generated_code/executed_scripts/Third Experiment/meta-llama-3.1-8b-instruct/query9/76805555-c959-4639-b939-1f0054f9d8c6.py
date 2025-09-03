import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the necessary information
            if "connections" in data and "followers_and_following" in data["connections"] and "close_friends.json" in data["connections"]["followers_and_following"]:
                # Load the close friends data
                close_friends_data = data["connections"]["followers_and_following"]["close_friends.json"]

                # Check if the close friends data contains the necessary information
                if "string_map_data" in close_friends_data["structure"][0] and "Vorname" in close_friends_data["structure"][0]["string_map_data"]:
                    # Extract the names of the profiles the user follows
                    followed_profiles = [profile["string_map_data"]["Vorname"]["value"] for profile in close_friends_data["structure"][0]["string_map_data"] if "Vorname" in profile["string_map_data"]]

                    # Iterate over the files in the root directory again
                    for filename in os.listdir(root_dir):
                        # Check if the file is a JSON file
                        if filename.endswith(".json"):
                            # Open the JSON file
                            with open(os.path.join(root_dir, filename), 'r') as file:
                                # Load the JSON data
                                data = eval(file.read())

                                # Check if the JSON data contains the necessary information
                                if "connections" in data and "followers_and_following" in data["connections"] and "close_friends.json" in data["connections"]["followers_and_following"]:
                                    # Load the close friends data
                                    close_friends_data = data["connections"]["followers_and_following"]["close_friends.json"]

                                    # Check if the close friends data contains the necessary information
                                    if "string_map_data" in close_friends_data["structure"][0] and "Vorname" in close_friends_data["structure"][0]["string_map_data"]:
                                        # Extract the names of the profiles that follow the user
                                        follower_profiles = [profile["string_map_data"]["Vorname"]["value"] for profile in close_friends_data["structure"][0]["string_map_data"] if "Vorname" in profile["string_map_data"]]

                                        # Find the profiles that do not follow the user back
                                        profiles.extend([profile for profile in followed_profiles if profile not in follower_profiles])

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Profile"])  # Write the column headers
    writer.writerows([[profile] for profile in profiles])  # Write the profiles