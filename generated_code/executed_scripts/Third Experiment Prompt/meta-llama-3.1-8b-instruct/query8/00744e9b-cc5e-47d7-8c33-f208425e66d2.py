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
            if "likes" in data and "media" in data["likes"]:
                for item in data["likes"]["media"]:
                    if "likes" in item and "story_likes" in item["likes"]:
                        result["User"].append(item["title"])
                        result["Post Likes"].append(item["likes"]["post_likes"])
                        result["Story Likes"].append(item["likes"]["story_likes"])
                        result["Comments"].append(item["likes"]["comments"])
            elif "likes" in data and "comment_likes" in data["likes"]:
                for item in data["likes"]["comment_likes"]:
                    result["User"].append(item["title"])
                    result["Post Likes"].append(0)
                    result["Story Likes"].append(0)
                    result["Comments"].append(item["likes"])
            elif "likes" in data and "story_likes" in data["likes"]:
                for item in data["likes"]["story_likes"]:
                    result["User"].append(item["title"])
                    result["Post Likes"].append(0)
                    result["Story Likes"].append(item["likes"])
                    result["Comments"].append(0)
            elif "likes" in data and "comment_likes" in data["likes"]:
                for item in data["likes"]["comment_likes"]:
                    result["User"].append(item["title"])
                    result["Post Likes"].append(0)
                    result["Story Likes"].append(0)
                    result["Comments"].append(item["likes"])
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON file {file_path}")

# Define the function to process the directory
def process_directory(directory):
    for item in os.listdir(directory):
        file_path = os.path.join(directory, item)
        if os.path.isfile(file_path) and item.endswith(".json"):
            process_json_file(file_path)
        elif os.path.isdir(file_path):
            process_directory(file_path)

# Process the root directory
process_directory(root_dir)

# Sort the result dictionary by the sum of Post Likes, Story Likes, and Comments
result["User"] = sorted(set(result["User"]), key=lambda x: sum([result["Post Likes"][result["User"].index(x)], result["Story Likes"][result["User"].index(x)], result["Comments"][result["User"].index(x)]]), reverse=True)[:20]

# Write the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user in result["User"]:
        writer.writerow([user, result["Post Likes"][result["User"].index(user)], result["Story Likes"][result["User"].index(user)], result["Comments"][result["User"].index(user)]])