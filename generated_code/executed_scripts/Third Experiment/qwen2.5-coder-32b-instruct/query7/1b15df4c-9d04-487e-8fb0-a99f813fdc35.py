import os
import csv
from collections import defaultdict

# Variable referring to the file input
root_dir = "root_dir"

# Function to check if the directory exists
def check_directory_exists(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"FileNotFoundError: The root directory {directory} does not exist.")

# Function to read JSON files and extract relevant data
def read_json_file(file_path):
    import json
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to process stories data and count engagements
def process_stories_data(stories_data):
    engagement_count = defaultdict(int)
    for story in stories_data.get('ig_stories', []):
        # Assuming the 'title' field contains the user's name or identifier
        user = story.get('title', 'Unknown User')
        engagement_count[user] += 1
    return engagement_count

# Main function to execute the script
def main():
    # Check if the root directory exists
    check_directory_exists(root_dir)
    
    # Define the path to the stories.json file
    stories_file_path = os.path.join(root_dir, 'your_instagram_activity', 'media', 'stories.json')
    
    # Read the stories.json file
    stories_data = read_json_file(stories_file_path)
    
    # Process the stories data to count engagements
    engagement_count = process_stories_data(stories_data)
    
    # Determine the user with the most engagements
    most_engaged_user = max(engagement_count, key=engagement_count.get, default='No User Engaged')
    most_engagements = engagement_count[most_engaged_user]
    
    # Prepare the CSV data
    csv_data = [('User', 'Times Engaged'), (most_engaged_user, most_engagements)]
    
    # Write the CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

# Execute the main function
if __name__ == "__main__":
    main()