import csv
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
        with open(file_path, 'r') as file:
            data = file.read()
            import json
            data = json.loads(data)
            if "likes_media_likes" in data["structure"]:
                for item in data["structure"]["likes_media_likes"]:
                    result["User"].append(item["title"])
                    result["Post Likes"].append(len(item["string_list_data"]))
            elif "story_activities_story_likes" in data["structure"]:
                for item in data["structure"]["story_activities_story_likes"]:
                    result["User"].append(item["title"])
                    result["Story Likes"].append(len(item["string_list_data"]))
            elif "likes_comment_likes" in data["structure"]:
                for item in data["structure"]["likes_comment_likes"]:
                    result["User"].append(item["title"])
                    result["Comments"].append(len(item["string_list_data"]))
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Define the function to process the directory
def process_directory(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            if item.endswith(".json"):
                process_json_file(item_path)
        elif os.path.isdir(item_path):
            process_directory(item_path)

# Process the root directory
process_directory(root_dir)

# Sort the result dictionary by the number of interactions
result["User"] = sorted(set(result["User"]))
result["Post Likes"] = sorted(result["Post Likes"], reverse=True)
result["Story Likes"] = sorted(result["Story Likes"], reverse=True)
result["Comments"] = sorted(result["Comments"], reverse=True)

# Write the result to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result["User"]))):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])