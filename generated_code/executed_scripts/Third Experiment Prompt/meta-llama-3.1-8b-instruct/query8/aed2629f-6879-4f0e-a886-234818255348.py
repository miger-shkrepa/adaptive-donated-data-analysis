import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the result dictionary
result = {"User": [], "Post Likes": [], "Story Likes": [], "Comments": []}

# Define the function to extract data from the JSON files
def extract_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            return data
    except Exception as e:
        print(f"Error: {e}")
        return None

# Define the function to process the data
def process_data(data):
    try:
        data = json.loads(data)
        # Extract the relevant data from the JSON file
        user = None
        post_likes = 0
        story_likes = 0
        comments = 0

        # Check if the data is a dictionary
        if isinstance(data, dict):
            # Check if the data has a 'username' key
            if 'username' in data:
                user = data['username']
            # Check if the data has a 'likes' key
            if 'likes' in data:
                # Check if the likes are a list
                if isinstance(data['likes'], list):
                    # Iterate over the likes
                    for like in data['likes']:
                        # Check if the like is a dictionary
                        if isinstance(like, dict):
                            # Check if the like has a 'type' key
                            if 'type' in like:
                                # Check if the like type is 'post'
                                if like['type'] == 'post':
                                    # Increment the post likes
                                    post_likes += 1
                                # Check if the like type is 'story'
                                elif like['type'] == 'story':
                                    # Increment the story likes
                                    story_likes += 1
                                # Check if the like type is 'comment'
                                elif like['type'] == 'comment':
                                    # Increment the comments
                                    comments += 1

        # Add the data to the result dictionary
        result["User"].append(user)
        result["Post Likes"].append(post_likes)
        result["Story Likes"].append(story_likes)
        result["Comments"].append(comments)
    except Exception as e:
        print(f"Error: {e}")

# Define the function to process the directory
def process_directory(directory):
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # Check if the file is a JSON file
                if file.endswith(".json"):
                    # Extract the data from the JSON file
                    data = extract_data(file_path)
                    if data:
                        # Process the data
                        process_data(data)
    except Exception as e:
        print(f"Error: {e}")

# Process the directory
process_directory(root_dir)

# Save the result to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result["User"]))):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])

print("Query completed successfully.")