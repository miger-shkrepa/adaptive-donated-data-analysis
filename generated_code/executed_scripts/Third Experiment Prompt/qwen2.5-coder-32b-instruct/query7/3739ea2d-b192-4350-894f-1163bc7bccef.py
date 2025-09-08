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

# Function to extract user engagement data from liked posts
def extract_story_likes(data):
    story_likes = defaultdict(int)
    if 'likes_media_likes' in data:
        for like in data['likes_media_likes']:
            for item in like['string_list_data']:
                if 'story' in item['value'].lower():
                    user = item['value'].split(' ')[0]  # Assuming the username is the first word in the value
                    story_likes[user] += 1
    return story_likes

# Main function to process the directory and generate the CSV
def process_directory(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the liked_posts.json file
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        
        # Initialize the dictionary to store story likes
        story_likes = defaultdict(int)
        
        # Check if the liked_posts.json file exists and process it
        if os.path.exists(liked_posts_path):
            liked_posts_data = read_json_file(liked_posts_path)
            story_likes.update(extract_story_likes(liked_posts_data['structure']))
        
        # Prepare the data for CSV
        sorted_story_likes = sorted(story_likes.items(), key=lambda x: x[1], reverse=True)
        
        # Define the output CSV file path
        output_csv_path = 'query_responses/results.csv'
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        
        # Write the data to the CSV file
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Times Engaged'])
            csvwriter.writerows(sorted_story_likes)
    
    except Exception as e:
        # If any error occurs, create an empty CSV with only headers
        output_csv_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['User', 'Times Engaged'])
        print(f"An error occurred: {e}")

# Execute the main function
process_directory(root_dir)