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
            if isinstance(data, dict) and "type" in data and data["type"] == "json":
                structure = data.get("structure")
                if structure and isinstance(structure, dict):
                    if "likes_media_likes" in structure:
                        for item in structure.get("likes_media_likes", []):
                            result["User"].append(item.get("title", ""))
                            result["Post Likes"].append(len(item.get("string_list_data", [])))
                    elif "story_activities_story_likes" in structure:
                        for item in structure.get("story_activities_story_likes", []):
                            result["User"].append(item.get("title", ""))
                            result["Story Likes"].append(len(item.get("string_list_data", [])))
                    elif "comments_reels_comments" in structure:
                        for item in structure.get("comments_reels_comments", []):
                            result["User"].append(item.get("title", ""))
                            result["Comments"].append(1)
                    elif "comments_post_comments_1" in structure:
                        for item in structure:
                            result["User"].append(item.get("title", ""))
                            result["Comments"].append(1)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON file.")

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
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result["User"]))):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])

# Print the result
print("Result saved to query_responses/results.csv")