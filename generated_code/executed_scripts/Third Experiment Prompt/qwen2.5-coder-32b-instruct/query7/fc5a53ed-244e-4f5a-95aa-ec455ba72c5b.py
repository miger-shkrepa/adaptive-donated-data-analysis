import os
import csv
from collections import defaultdict

# Variable referring to the file input
root_dir = "root_dir"

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            import json
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to count story likes per user
def count_story_likes(data):
    user_likes = defaultdict(int)
    for entry in data.get('story_activities_story_likes', []):
        for item in entry.get('string_list_data', []):
            if 'href' in item:
                user_likes[item['href']] += 1
    return user_likes

# Main function to process the data and generate the CSV
def main():
    # Define the path to the story_likes.json file
    story_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
    
    # Check if the file exists
    if not os.path.exists(story_likes_path):
        # If the file does not exist, create an empty CSV with headers
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
        return
    
    # Read the story_likes.json file
    story_likes_data = read_json_file(story_likes_path)
    
    # Count the likes per user
    user_likes = count_story_likes(story_likes_data)
    
    # Sort the users by the number of likes in descending order
    sorted_users = sorted(user_likes.items(), key=lambda x: x[1], reverse=True)
    
    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
        for user, count in sorted_users:
            writer.writerow([user, count])

# Execute the main function
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)