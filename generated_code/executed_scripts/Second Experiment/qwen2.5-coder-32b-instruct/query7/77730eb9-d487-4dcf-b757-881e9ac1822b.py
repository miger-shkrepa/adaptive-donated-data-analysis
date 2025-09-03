import os
import csv
import json

root_dir = "root_dir"

def get_user_story_engagement(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        stories_engagement = {}
        
        # Check if the required directory exists
        stories_dir = os.path.join(root_dir, "personal_information", "instagram_profile_information.json")
        if not os.path.exists(stories_dir):
            # If the file is missing, return an empty CSV with headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User', 'Times Engaged'])
            return
        
        with open(stories_dir, 'r') as file:
            data = json.load(file)
        
        if 'profile_account_insights' in data:
            for entry in data['profile_account_insights']:
                if 'string_map_data' in entry:
                    first_story_time = entry['string_map_data'].get('First Story Time', {}).get('value', None)
                    last_story_time = entry['string_map_data'].get('Last Story Time', {}).get('value', None)
                    
                    if first_story_time and last_story_time:
                        # Assuming the value is in a format that can be compared or counted
                        # Here we just count the number of entries as an example of engagement
                        user = entry['string_map_data'].get('First Close Friends Story Time', {}).get('value', 'Unknown User')
                        if user in stories_engagement:
                            stories_engagement[user] += 1
                        else:
                            stories_engagement[user] = 1
        
        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            for user, count in stories_engagement.items():
                writer.writerow([user, count])
    
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while processing the data: {str(e)}")

get_user_story_engagement(root_dir)