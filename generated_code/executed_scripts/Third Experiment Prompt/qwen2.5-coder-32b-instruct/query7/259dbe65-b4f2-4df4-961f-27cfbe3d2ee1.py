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
    
    engagement_counts = defaultdict(int)
    
    for entry in story_likes_data.get("story_activities_story_likes", []):
        for item in entry.get("string_list_data", []):
            if "href" in item:
                # Extract the username from the href
                username = item["href"].split("/")[-2]
                engagement_counts[username] += 1
    
    return engagement_counts

# Main function to generate the CSV
def generate_csv(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    engagement_counts = count_story_interactions(root_dir)
    
    # Sort the engagement counts by the number of engagements in descending order
    sorted_engagements = sorted(engagement_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Write the results to a CSV file
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["User", "Times Engaged"])
        csvwriter.writerows(sorted_engagements)

# Execute the main function
try:
    generate_csv(root_dir)
except Exception as e:
    print(e)