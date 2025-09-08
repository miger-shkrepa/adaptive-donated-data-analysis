import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to load JSON data from a file
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to process story interactions and count engagements
def process_story_interactions(story_likes_path):
    story_engagements = {}
    
    if not os.path.exists(story_likes_path):
        return story_engagements
    
    try:
        data = load_json(story_likes_path)
        story_activities = data.get("story_activities_story_likes", [])
        
        for activity in story_activities:
            string_list_data = activity.get("string_list_data", [])
            for item in string_list_data:
                value = item.get("value")
                if value:
                    if value in story_engagements:
                        story_engagements[value] += 1
                    else:
                        story_engagements[value] = 1
    except Exception as e:
        raise ValueError(f"Error: Failed to process story interactions - {str(e)}")
    
    return story_engagements

# Main function to generate the CSV file
def generate_csv():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        
        story_engagements = process_story_interactions(story_likes_path)
        
        # Sort the engagements by count in descending order
        sorted_engagements = sorted(story_engagements.items(), key=lambda x: x[1], reverse=True)
        
        # Write the results to a CSV file
        csv_file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            
            if sorted_engagements:
                for user, count in sorted_engagements:
                    writer.writerow([user, count])
            else:
                writer.writerow(['', ''])
        
        print(f"CSV file saved at {csv_file_path}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Execute the main function
generate_csv()