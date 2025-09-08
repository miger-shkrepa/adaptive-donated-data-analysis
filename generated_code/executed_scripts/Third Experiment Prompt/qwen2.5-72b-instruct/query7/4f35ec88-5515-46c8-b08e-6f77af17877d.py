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
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from the specified file.")

# Function to count story interactions
def count_story_interactions(root_dir):
    story_interactions = {}
    
    story_interactions_dir = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions')
    
    if not os.path.exists(story_interactions_dir):
        return story_interactions
    
    for file_name in os.listdir(story_interactions_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(story_interactions_dir, file_name)
            data = load_json(file_path)
            
            if 'story_activities_questions' in data:
                for entry in data['story_activities_questions']:
                    for item in entry['string_list_data']:
                        user = item['value']
                        if user in story_interactions:
                            story_interactions[user] += 1
                        else:
                            story_interactions[user] = 1
    
    return story_interactions

# Main function to generate the CSV file
def generate_csv(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_interactions = count_story_interactions(root_dir)
        
        # Prepare the CSV file path
        csv_file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        
        # Write the CSV file
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for user, count in story_interactions.items():
                writer.writerow({'User': user, 'Times Engaged': count})
        
        print(f"CSV file saved at {csv_file_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Execute the main function
generate_csv(root_dir)