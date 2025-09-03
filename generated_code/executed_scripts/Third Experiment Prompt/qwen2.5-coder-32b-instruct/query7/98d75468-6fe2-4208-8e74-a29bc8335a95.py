import os
import csv
import json
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return its content
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
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
    
    engagement_count = defaultdict(int)
    
    for entry in story_likes_data.get("story_activities_story_likes", []):
        for item in entry.get("string_list_data", []):
            if "value" in item:
                engagement_count[item["value"]] += 1
    
    return engagement_count

# Main function to generate the CSV file
def generate_csv(root_dir):
    engagement_count = count_story_interactions(root_dir)
    
    # Sort the engagement count by the number of interactions in descending order
    sorted_engagement = sorted(engagement_count.items(), key=lambda x: x[1], reverse=True)
    
    # Write the results to a CSV file
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["User", "Times Engaged"])
        csvwriter.writerows(sorted_engagement)

# Execute the main function
try:
    generate_csv(root_dir)
except Exception as e:
    print(f"Error: {e}")