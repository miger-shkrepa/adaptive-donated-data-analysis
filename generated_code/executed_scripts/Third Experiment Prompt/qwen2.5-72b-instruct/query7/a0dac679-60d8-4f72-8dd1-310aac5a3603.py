import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def process_story_interactions(data, interactions):
    if 'story_activities_questions' in data:
        for entry in data['story_activities_questions']:
            for item in entry['string_list_data']:
                interactions[item['value']] = interactions.get(item['value'], 0) + 1

    if 'story_activities_polls' in data:
        for entry in data['story_activities_polls']:
            for item in entry['string_list_data']:
                interactions[item['value']] = interactions.get(item['value'], 0) + 1

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        story_interactions_dir = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions')
        if not os.path.exists(story_interactions_dir):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User', 'Times Engaged'])
            return

        interactions = {}
        for filename in ['polls.json', 'questions.json']:
            file_path = os.path.join(story_interactions_dir, filename)
            if os.path.exists(file_path):
                data = load_json_file(file_path)
                process_story_interactions(data, interactions)

        if not interactions:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User', 'Times Engaged'])
            return

        most_engaged_user = max(interactions, key=interactions.get)
        most_engaged_count = interactions[most_engaged_user]

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            writer.writerow([most_engaged_user, most_engaged_count])

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()