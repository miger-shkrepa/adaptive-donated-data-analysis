import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the result dictionary
result = {"User": [], "Post Likes": [], "Story Likes": [], "Comments": []}

# Define the function to process the JSON files
def process_json_file(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            if "structure" in data:
                if "likes_media_likes" in data["structure"]:
                    for item in data["structure"]["likes_media_likes"]:
                        user = item["title"]
                        post_likes = len(item["string_list_data"])
                        result["User"].append(user)
                        result["Post Likes"].append(post_likes)
                        result["Story Likes"].append(0)
                        result["Comments"].append(0)
                elif "story_activities_story_likes" in data["structure"]:
                    for item in data["structure"]["story_activities_story_likes"]:
                        user = item["title"]
                        story_likes = len(item["string_list_data"])
                        result["User"].append(user)
                        result["Post Likes"].append(0)
                        result["Story Likes"].append(story_likes)
                        result["Comments"].append(0)
                elif "comments_reels_comments" in data["structure"]:
                    for item in data["structure"]["comments_reels_comments"]:
                        user = item["string_map_data"]["Media Owner"]["value"]
                        comments = len(item["string_map_data"]["Comment"]["value"])
                        result["User"].append(user)
                        result["Post Likes"].append(0)
                        result["Story Likes"].append(0)
                        result["Comments"].append(comments)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON in file {file_path}.")

# Define the function to process the directory
def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".json"):
                process_json_file(file_path)

# Process the directory
process_directory(root_dir)

# Save the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result["User"]))):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])