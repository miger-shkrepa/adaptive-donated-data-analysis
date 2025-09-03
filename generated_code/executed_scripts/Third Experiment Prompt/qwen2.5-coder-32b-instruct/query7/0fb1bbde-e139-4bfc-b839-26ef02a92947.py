import os
import csv
from collections import defaultdict

# Variable referring to the file input
root_dir = "root_dir"

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return eval(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")

# Function to count story interactions
def count_story_interactions(root_dir):
    story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
    
    if not os.path.exists(story_likes_path):
        return defaultdict(int)
    
    story_likes_data = read_json_file(story_likes_path)
    
    if "story_activities_story_likes" not in story_likes_data:
        return defaultdict(int)
    
    interactions_count = defaultdict(int)
    
    for entry in story_likes_data["story_activities_story_likes"]:
        for item in entry.get("string_list_data", []):
            if "value" in item:
                interactions_count[item["value"]] += 1
    
    return interactions_count

# Main function to generate the CSV
def generate_csv(root_dir):
    interactions_count = count_story_interactions(root_dir)
    
    # Sort by the number of interactions in descending order
    sorted_interactions = sorted(interactions_count.items(), key=lambda x: x[1], reverse=True)
    
    # Write to CSV
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['User', 'Times Engaged'])
        for user, count in sorted_interactions:
            csvwriter.writerow([user, count])

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Generate the CSV
generate_csv(root_dir)