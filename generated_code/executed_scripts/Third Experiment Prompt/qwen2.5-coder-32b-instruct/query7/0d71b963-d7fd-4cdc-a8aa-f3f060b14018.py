import os
import csv
from collections import defaultdict

# Variable referring to the file input
root_dir = "root_dir"

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            import json
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to count story interactions
def count_story_interactions(root_dir):
    story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
    
    if not os.path.exists(story_likes_path):
        return defaultdict(int)
    
    story_likes_data = read_json_file(story_likes_path)
    
    story_likes_count = defaultdict(int)
    
    for story_like in story_likes_data.get("story_activities_story_likes", []):
        for item in story_like.get("string_list_data", []):
            if "href" in item:
                username = item["href"].split("/")[-2]
                story_likes_count[username] += 1
    
    return story_likes_count

# Main function to generate the CSV file
def generate_csv(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    story_likes_count = count_story_interactions(root_dir)
    
    # Determine the user with the most story interactions
    most_engaged_user = max(story_likes_count, key=story_likes_count.get, default=None)
    most_engaged_times = story_likes_count[most_engaged_user] if most_engaged_user else 0
    
    # Prepare the CSV data
    csv_data = [("User", "Times Engaged")]
    if most_engaged_user:
        csv_data.append((most_engaged_user, most_engaged_times))
    
    # Write the CSV file
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(csv_data)

# Execute the main function
generate_csv(root_dir)