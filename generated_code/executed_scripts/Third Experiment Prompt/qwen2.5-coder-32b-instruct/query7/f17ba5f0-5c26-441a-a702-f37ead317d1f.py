import os
import csv
from collections import defaultdict

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files and extract relevant data
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = eval(file.read())
            return data
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
    
    interaction_counts = defaultdict(int)
    
    try:
        for entry in story_likes_data.get("story_activities_story_likes", []):
            for item in entry.get("string_list_data", []):
                if "value" in item:
                    interaction_counts[item["value"]] += 1
    except Exception as e:
        raise ValueError(f"ValueError: Error processing story_likes.json: {str(e)}")
    
    return interaction_counts

# Main function to generate the CSV file
def generate_csv(root_dir):
    interaction_counts = count_story_interactions(root_dir)
    
    # Prepare the CSV file
    csv_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["User", "Times Engaged"])
        
        for user, count in interaction_counts.items():
            csvwriter.writerow([user, count])

# Execute the main function
try:
    generate_csv(root_dir)
except Exception as e:
    print(f"Error: {str(e)}")