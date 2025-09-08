import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def count_story_engagements(data):
    story_engagements = {}
    for story_activity in data:
        for entry in story_activity.get("string_list_data", []):
            author = entry.get("value")
            if author:
                story_engagements[author] = story_engagements.get(author, 0) + 1
    return story_engagements

def process_story_interactions(directory):
    story_engagements = {}
    story_interaction_files = ["polls.json", "questions.json", "quizzes.json", "story_likes.json"]
    
    for file_name in story_interaction_files:
        file_path = os.path.join(directory, file_name)
        if not os.path.exists(file_path):
            continue
        
        data = load_json_file(file_path)
        story_data = data.get(f"story_activities_{file_name.split('.')[0]}", [])
        engagements = count_story_engagements(story_data)
        
        for author, count in engagements.items():
            story_engagements[author] = story_engagements.get(author, 0) + count
    
    return story_engagements

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")
    if not os.path.exists(story_interactions_dir):
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
        return
    
    story_engagements = process_story_interactions(story_interactions_dir)
    
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, count in story_engagements.items():
            writer.writerow([user, count])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)