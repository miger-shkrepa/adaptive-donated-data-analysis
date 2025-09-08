import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the result dictionary
result = {"User": [], "Post Likes": [], "Story Likes": [], "Comments": []}

# Define the function to process the JSON files
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'type' in data and data['type'] == 'json':
                structure = data.get('structure', {})
                if 'likes_media_likes' in structure:
                    for item in structure.get('likes_media_likes', []):
                        if 'string_list_data' in item:
                            for item2 in item['string_list_data']:
                                if 'href' in item2 and 'timestamp' in item2:
                                    result['User'].append(item2['href'])
                                    result['Post Likes'].append(item2['timestamp'])
                elif 'story_activities_story_likes' in structure:
                    for item in structure.get('story_activities_story_likes', []):
                        if 'string_list_data' in item:
                            for item2 in item['string_list_data']:
                                if 'timestamp' in item2:
                                    result['User'].append('story')
                                    result['Story Likes'].append(item2['timestamp'])
                elif 'likes_comment_likes' in structure:
                    for item in structure.get('likes_comment_likes', []):
                        if 'string_list_data' in item:
                            for item2 in item['string_list_data']:
                                if 'href' in item2 and 'timestamp' in item2:
                                    result['User'].append(item2['href'])
                                    result['Comments'].append(item2['timestamp'])
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON in file {file_path}.")

# Define the function to process the directory
def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.json'):
                process_json_file(file_path)

# Process the directory
process_directory(root_dir)

# Save the result to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result['User']))):
        writer.writerow([result['User'][i], result['Post Likes'][i], result['Story Likes'][i], result['Comments'][i]])

# Sort the result by Post Likes, Story Likes and Comments
result['Post Likes'] = sorted(result['Post Likes'])
result['Story Likes'] = sorted(result['Story Likes'])
result['Comments'] = sorted(result['Comments'])

# Save the sorted result to a CSV file
with open('query_responses/results.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(min(20, len(result['User']))):
        writer.writerow([result['User'][i], result['Post Likes'][i], result['Story Likes'][i], result['Comments'][i]])