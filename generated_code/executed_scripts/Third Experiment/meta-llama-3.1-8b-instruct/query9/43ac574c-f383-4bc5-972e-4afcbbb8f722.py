import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the profiles
profiles = []

# Iterate over the relationships_permanent_follow_requests
for relationship in ["relationships_permanent_follow_requests"]:
    # Check if the relationship exists
    if relationship in os.listdir(root_dir):
        # Iterate over the media_list_data
        for media in ["media_list_data"]:
            # Check if the media exists
            if media in os.listdir(os.path.join(root_dir, relationship)):
                # Iterate over the string_list_data
                for string in ["string_list_data"]:
                    # Check if the string exists
                    if string in os.listdir(os.path.join(root_dir, relationship, media)):
                        # Iterate over the href, timestamp, and value
                        for item in os.listdir(os.path.join(root_dir, relationship, media, string)):
                            # Check if the item exists
                            if item in os.listdir(os.path.join(root_dir, relationship, media, string)):
                                # Open the file and read the contents
                                with open(os.path.join(root_dir, relationship, media, string, item), 'r') as file:
                                    # Read the contents of the file
                                    data = file.read()
                                    # Check if the data is not empty
                                    if data:
                                        # Parse the JSON data
                                        import json
                                        data = json.loads(data)
                                        # Iterate over the value
                                        for value in data:
                                            # Check if the value is not empty
                                            if value:
                                                # Extract the profile
                                                profile = value['value']
                                                # Add the profile to the list
                                                profiles.append(profile)
                                    else:
                                        # If the data is empty, treat it as 0
                                        profiles.append(0)
                        # Iterate over the title
                        for title in ["title"]:
                            # Check if the title exists
                            if title in os.listdir(os.path.join(root_dir, relationship, media, string)):
                                # Open the file and read the contents
                                with open(os.path.join(root_dir, relationship, media, string, title), 'r') as file:
                                    # Read the contents of the file
                                    data = file.read()
                                    # Check if the data is not empty
                                    if data:
                                        # Parse the JSON data
                                        import json
                                        data = json.loads(data)
                                        # Iterate over the title
                                        for title in data:
                                            # Check if the title is not empty
                                            if title:
                                                # Extract the profile
                                                profile = title
                                                # Add the profile to the list
                                                profiles.append(profile)
                                    else:
                                        # If the data is empty, treat it as 0
                                        profiles.append(0)
                # Iterate over the media_map_data
                for media in ["media_map_data"]:
                    # Check if the media exists
                    if media in os.listdir(os.path.join(root_dir, relationship, string)):
                        # Iterate over the Profile Photo
                        for photo in ["Profile Photo"]:
                            # Check if the photo exists
                            if photo in os.listdir(os.path.join(root_dir, relationship, string, media)):
                                # Open the file and read the contents
                                with open(os.path.join(root_dir, relationship, string, media, photo), 'r') as file:
                                    # Read the contents of the file
                                    data = file.read()
                                    # Check if the data is not empty
                                    if data:
                                        # Parse the JSON data
                                        import json
                                        data = json.loads(data)
                                        # Iterate over the creation_timestamp, cross_post_source, media_metadata, title, and uri
                                        for item in data:
                                            # Check if the item exists
                                            if item:
                                                # Extract the profile
                                                profile = item['title']
                                                # Add the profile to the list
                                                profiles.append(profile)
                                    else:
                                        # If the data is empty, treat it as 0
                                        profiles.append(0)

# Write the profiles to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Profile"])
    writer.writerows([[profile] for profile in profiles])

print("The profiles that the user follows but do not follow back are:")
print(profiles)