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
            # Process the data
            if "likes_media_likes" in data["structure"]:
                for item in data["structure"]["likes_media_likes"]:
                    result["User"].append(item["title"])
                    result["Post Likes"].append(len(item["string_list_data"]))
            if "story_activities_story_likes" in data["structure"]:
                for item in data["structure"]["story_activities_story_likes"]:
                    result["User"].append(item["title"])
                    result["Story Likes"].append(len(item["string_list_data"]))
            if "comments_reels_comments" in data["structure"]:
                for item in data["structure"]["comments_reels_comments"]:
                    result["User"].append(item["string_map_data"]["Media Owner"]["value"])
                    result["Comments"].append(len(item["string_map_data"]["Comment"]["value"]))
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Walk through the directory and process the JSON files
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            process_json_file(file_path)

# Save the result to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result["User"]))):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])