import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    user_engagement = {}
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Iterate over the files in the root directory
    for filename in os.listdir(root_dir):
        file_path = os.path.join(root_dir, filename)
        
        # Check if the file is a directory
        if os.path.isdir(file_path):
            # Check if the directory is 'media'
            if filename == 'media':
                # Iterate over the subdirectories in the 'media' directory
                for subdirectory in os.listdir(file_path):
                    subdirectory_path = os.path.join(file_path, subdirectory)
                    
                    # Check if the subdirectory is 'posts'
                    if subdirectory == 'posts':
                        # Iterate over the files in the 'posts' directory
                        for file in os.listdir(subdirectory_path):
                            file_path = os.path.join(subdirectory_path, file)
                            
                            # Check if the file is a JSON file
                            if file.endswith('.json'):
                                try:
                                    with open(file_path, 'r') as f:
                                        data = json.load(f)
                                        
                                        # Check if the JSON file has the required structure
                                        if 'story_activities' in data:
                                            for activity in data['story_activities']:
                                                if 'title' in activity:
                                                    user = activity['title']
                                                    if user not in user_engagement:
                                                        user_engagement[user] = 1
                                                    else:
                                                        user_engagement[user] += 1
                                except json.JSONDecodeError:
                                    raise ValueError("ValueError: The JSON file is not valid.")
                            else:
                                # If the file is not a JSON file, skip it
                                continue
                    else:
                        # If the subdirectory is not 'posts', skip it
                        continue
            else:
                # If the directory is not 'media', skip it
                continue
        else:
            # If the file is not a directory, skip it
            continue
    
    return user_engagement

def save_to_csv(user_engagement):
    with open('query_responses/results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['User', 'Times Engaged'])
        
        # Check if user_engagement is empty
        if user_engagement:
            for user, engagement in user_engagement.items():
                writer.writerow([user, engagement])
        else:
            # If user_engagement is empty, write only the column headers
            pass

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        save_to_csv(user_engagement)
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['User', 'Times Engaged'])
    except ValueError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['User', 'Times Engaged'])

if __name__ == "__main__":
    main()