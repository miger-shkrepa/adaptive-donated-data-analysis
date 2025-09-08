import os
import csv
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
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
    
    engagement_count = defaultdict(int)
    
    try:
        for story_like in story_likes_data.get("story_activities_story_likes", []):
            for string_list_data in story_like.get("string_list_data", []):
                if "value" in string_list_data:
                    username = string_list_data["value"]
                    engagement_count[username] += 1
    except Exception as e:
        raise ValueError(f"ValueError: Error processing story_likes.json: {str(e)}")
    
    return engagement_count

# Main function to generate the CSV
def generate_csv(root_dir):
    engagement_count = count_story_interactions(root_dir)
    
    # Prepare the CSV data
    csv_data = [["User", "Times Engaged"]]
    for user, count in engagement_count.items():
        csv_data.append([user, count])
    
    # Write the CSV file
    try:
        os.makedirs(os.path.dirname('query_responses/results.csv'), exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)
    except Exception as e:
        raise ValueError(f"ValueError: Error writing the CSV file: {str(e)}")

# Execute the main function
try:
    generate_csv(root_dir)
except Exception as e:
    print(f"Error: {str(e)}")