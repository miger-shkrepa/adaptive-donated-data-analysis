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
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The specified JSON file is not properly formatted.")

# Function to process story likes and count user engagements
def process_story_likes(data):
    user_engagement = {}
    try:
        story_activities = data.get("story_activities_story_likes", [])
        for activity in story_activities:
            string_list_data = activity.get("string_list_data", [])
            for item in string_list_data:
                href = item.get("href", "")
                if href:
                    username = href.split('/')[-1]
                    if username in user_engagement:
                        user_engagement[username] += 1
                    else:
                        user_engagement[username] = 1
    except Exception as e:
        raise ValueError(f"Error: Failed to process story likes data. {str(e)}")
    return user_engagement

# Main function to generate the CSV file
def generate_csv():
    try:
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        if not os.path.exists(story_likes_path):
            # If the required file does not exist, return a CSV file with only headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User', 'Times Engaged'])
            return
        
        story_likes_data = read_json_file(story_likes_path)
        user_engagement = process_story_likes(story_likes_data)
        
        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            for user, count in user_engagement.items():
                writer.writerow([user, count])
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Execute the main function
if __name__ == "__main__":
    generate_csv()