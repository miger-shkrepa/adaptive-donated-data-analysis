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
    engagements = {}
    for story_type in ['story_activities_questions', 'story_activities_polls', 'story_activities_emoji_sliders', 'story_activities_quizzes', 'story_activities_story_likes']:
        if story_type in data:
            for entry in data[story_type]:
                for item in entry.get('string_list_data', []):
                    username = item.get('value')
                    if username:
                        if username not in engagements:
                            engagements[username] = 0
                        engagements[username] += 1
    return engagements

def process_story_interactions(root_dir):
    story_interactions_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions')
    if not os.path.exists(story_interactions_path):
        return {}

    engagements = {}
    for filename in ['questions.json', 'polls.json', 'emoji_sliders.json', 'quizzes.json', 'story_likes.json']:
        file_path = os.path.join(story_interactions_path, filename)
        if os.path.exists(file_path):
            try:
                data = load_json_file(file_path)
                engagements.update(count_story_engagements(data))
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return engagements

def write_csv(engagements):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
        for user, count in engagements.items():
            writer.writerow([user, count])

def main():
    if root_dir == "root_dir":
        raise ValueError("Error: The root directory placeholder 'root_dir' has not been replaced with an actual path.")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        engagements = process_story_interactions(root_dir)
        write_csv(engagements)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()