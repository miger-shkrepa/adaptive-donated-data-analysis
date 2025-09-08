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

# Define the function to process the JSON files
def process_json_file(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            # Process the JSON data
            if "structure" in data:
                for item in data["structure"]:
                    if "likes_media_likes" in item:
                        result["Post Likes"].append(item["title"])
                    elif "story_activities_story_likes" in item:
                        result["Story Likes"].append(item["title"])
                    elif "comments_reels_comments" in item:
                        result["Comments"].append(item["title"])
            else:
                # If the JSON file does not have a 'structure' key, treat it as a single item
                if "likes_media_likes" in data:
                    result["Post Likes"].append(data["likes_media_likes"][0]["title"])
                elif "story_activities_story_likes" in data:
                    result["Story Likes"].append(data["story_activities_story_likes"][0]["title"])
                elif "comments_reels_comments" in data:
                    result["Comments"].append(data["comments_reels_comments"][0]["title"])
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

# Print the top 20 users
print("Top 20 users:")
for i in range(min(20, len(result["User"]))):
    print(f"{result['User'][i]}: {result['Post Likes'][i]} post likes, {result['Story Likes'][i]} story likes, {result['Comments'][i]} comments")