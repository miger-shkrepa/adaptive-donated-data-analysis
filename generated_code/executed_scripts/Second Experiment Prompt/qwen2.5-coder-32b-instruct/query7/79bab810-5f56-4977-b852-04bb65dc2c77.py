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

# Function to count story engagements
def count_story_engagements(root_dir):
    story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
    
    if not os.path.exists(story_likes_path):
        return defaultdict(int)
    
    story_likes_data = read_json_file(story_likes_path)
    
    engagement_counts = defaultdict(int)
    
    try:
        for story_like in story_likes_data.get("story_activities_story_likes", []):
            for item in story_like.get("string_list_data", []):
                if "href" in item:
                    username = item["href"].split("/")[-1]
                    engagement_counts[username] += 1
    except Exception as e:
        raise ValueError(f"ValueError: Error processing story_likes.json: {str(e)}")
    
    return engagement_counts

# Main function to generate the CSV
def generate_csv(root_dir):
    engagement_counts = count_story_engagements(root_dir)
    
    # Sort the engagements by count in descending order
    sorted_engagements = sorted(engagement_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Write the results to a CSV file
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Times Engaged'])
            csvwriter.writerows(sorted_engagements)
    except Exception as e:
        raise ValueError(f"ValueError: Error writing to CSV file: {str(e)}")

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Generate the CSV
generate_csv(root_dir)