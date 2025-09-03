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

            # Check if the JSON data contains the 'likes' or 'saved' key
            if 'likes' in data or 'saved' in data:
                # Iterate over the likes or saved posts
                for post in data['likes'].get('liked_posts.json', {}).get('structure', {}).get('likes_media_likes', []) + data['saved'].get('saved_posts.json', {}).get('structure', {}).get('saved_saved_media', []):
                    # Check if the post contains the 'string_list_data' or 'string_map_data' key
                    if 'string_list_data' in post or 'string_map_data' in post:
                        # Iterate over the string list data or string map data
                        for item in post.get('string_list_data', []) + post.get('string_map_data', {}).values():
                            # Check if the item contains the 'href' key
                            if 'href' in item:
                                # Extract the profile from the href
                                profile = item['href']

                                # Check if the profile is not the same as the current user
                                if profile != 'current_user':
                                    # Add the profile to the list
                                    profiles.append(profile)

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Profile'])  # Write the header
    writer.writerows([[profile] for profile in profiles])  # Write the profiles

print("Query completed successfully.")