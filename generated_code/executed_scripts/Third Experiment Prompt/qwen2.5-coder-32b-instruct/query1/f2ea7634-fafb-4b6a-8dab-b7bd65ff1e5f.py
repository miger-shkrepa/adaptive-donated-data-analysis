import os
import json
import csv

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

# Function to extract topics from liked posts
def extract_topics_from_likes(likes_data):
    topics = set()
    if likes_data and 'likes_media_likes' in likes_data:
        for item in likes_data['likes_media_likes']:
            if 'string_list_data' in item:
                for data in item['string_list_data']:
                    if 'value' in data:
                        topics.add(data['value'])
    return topics

# Function to extract topics from saved posts
def extract_topics_from_saved(saved_data):
    topics = set()
    if saved_data and 'saved_saved_media' in saved_data:
        for item in saved_data['saved_saved_media']:
            if 'title' in item:
                topics.add(item['title'])
    return topics

# Main function to process the directory and generate the CSV
def generate_topics_of_interest_csv(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Initialize topics set
        topics_of_interest = set()
        
        # Path to liked posts JSON file
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            likes_data = read_json_file(liked_posts_path)
            topics_of_interest.update(extract_topics_from_likes(likes_data))
        
        # Path to saved posts JSON file
        saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
        if os.path.exists(saved_posts_path):
            saved_data = read_json_file(saved_posts_path)
            topics_of_interest.update(extract_topics_from_saved(saved_data))
        
        # Write the topics to a CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    
    except Exception as e:
        # Write only the column headers if an error occurs
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])

# Execute the main function
generate_topics_of_interest_csv(root_dir)