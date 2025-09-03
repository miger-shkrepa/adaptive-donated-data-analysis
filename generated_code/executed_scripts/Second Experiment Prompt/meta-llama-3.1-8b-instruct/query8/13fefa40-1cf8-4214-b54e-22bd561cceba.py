import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the result dictionary
result = {"User": [], "Post Likes": [], "Story Likes": [], "Comments": []}

# Define the function to process the data
def process_data(root_dir):
    # Iterate over the files in the root directory
    for filename in os.listdir(root_dir):
        # Construct the full path to the file
        filepath = os.path.join(root_dir, filename)

        # Check if the file is a JSON file
        if filename.endswith(".json"):
            # Open the JSON file
            with open(filepath, 'r') as file:
                # Load the JSON data
                data = json.load(file)

                # Process the data
                process_json_data(data, result)

# Define the function to process the JSON data
def process_json_data(data, result):
    # Check if the data is a dictionary
    if isinstance(data, dict):
        # Iterate over the items in the dictionary
        for key, value in data.items():
            # Check if the value is a list
            if isinstance(value, list):
                # Iterate over the items in the list
                for item in value:
                    # Check if the item is a dictionary
                    if isinstance(item, dict):
                        # Process the item
                        process_item(item, result)

# Define the function to process an item
def process_item(item, result):
    # Check if the item has a "string_map_data" key
    if "string_map_data" in item:
        # Get the string map data
        string_map_data = item["string_map_data"]

        # Check if the string map data has a "Post Likes" key
        if "Post Likes" in string_map_data:
            # Get the post likes value
            post_likes = string_map_data["Post Likes"]["value"]

            # Check if the post likes value is a string
            if isinstance(post_likes, str):
                # Add the post likes value to the result dictionary
                result["Post Likes"].append(post_likes)

        # Check if the string map data has a "Story Likes" key
        if "Story Likes" in string_map_data:
            # Get the story likes value
            story_likes = string_map_data["Story Likes"]["value"]

            # Check if the story likes value is a string
            if isinstance(story_likes, str):
                # Add the story likes value to the result dictionary
                result["Story Likes"].append(story_likes)

        # Check if the string map data has a "Comments" key
        if "Comments" in string_map_data:
            # Get the comments value
            comments = string_map_data["Comments"]["value"]

            # Check if the comments value is a string
            if isinstance(comments, str):
                # Add the comments value to the result dictionary
                result["Comments"].append(comments)

# Define the function to get the top 20 users
def get_top_users(result):
    # Create a dictionary to store the user interactions
    user_interactions = {}

    # Iterate over the result dictionary
    for i in range(len(result["User"])):
        # Get the user and their interactions
        user = result["User"][i]
        post_likes = result["Post Likes"][i]
        story_likes = result["Story Likes"][i]
        comments = result["Comments"][i]

        # Add the user interactions to the dictionary
        if user not in user_interactions:
            user_interactions[user] = {"Post Likes": 0, "Story Likes": 0, "Comments": 0}

        # Update the user interactions
        user_interactions[user]["Post Likes"] += int(post_likes)
        user_interactions[user]["Story Likes"] += int(story_likes)
        user_interactions[user]["Comments"] += int(comments)

    # Sort the user interactions in descending order
    sorted_users = sorted(user_interactions.items(), key=lambda x: (x[1]["Post Likes"] + x[1]["Story Likes"] + x[1]["Comments"]), reverse=True)

    # Get the top 20 users
    top_users = sorted_users[:20]

    # Return the top 20 users
    return top_users

# Process the data
process_data(root_dir)

# Get the top 20 users
top_users = get_top_users(result)

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])

    # Write the top 20 users
    for user, interactions in top_users:
        writer.writerow([user, interactions["Post Likes"], interactions["Story Likes"], interactions["Comments"]])