import os
import csv
import json

root_dir = "root_dir"

def get_user_engagement(root_directory):
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        engagement_data = {}
        
        # Navigate to the stories directory
        stories_dir = os.path.join(root_directory, 'stories')
        if not os.path.exists(stories_dir):
            return engagement_data
        
        # Iterate through each story file in the stories directory
        for story_file in os.listdir(stories_dir):
            story_path = os.path.join(stories_dir, story_file)
            if os.path.isfile(story_path) and story_file.endswith('.json'):
                with open(story_path, 'r', encoding='utf-8') as file:
                    story_data = json.load(file)
                    for story in story_data.get('story_activities_story_likes', []):
                        for data in story.get('string_list_data', []):
                            timestamp = data.get('timestamp')
                            if timestamp:
                                user = story.get('title')
                                if user in engagement_data:
                                    engagement_data[user] += 1
                                else:
                                    engagement_data[user] = 1
        return engagement_data
    
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while processing the data - {str(e)}")

def save_to_csv(engagement_data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            for user, times in engagement_data.items():
                writer.writerow([user, times])
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while writing to CSV - {str(e)}")

# Main execution
try:
    engagement_data = get_user_engagement(root_dir)
    save_to_csv(engagement_data, 'query_responses/results.csv')
except Exception as e:
    print(e)
    save_to_csv({}, 'query_responses/results.csv')