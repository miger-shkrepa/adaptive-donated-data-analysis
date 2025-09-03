import os
import json
import csv

root_dir = "root_dir"

def process_story_interactions(directory):
    user_engagement = {}
    story_interactions_path = os.path.join(directory, "story_interactions")

    if not os.path.exists(story_interactions_path):
        return user_engagement

    for filename in os.listdir(story_interactions_path):
        if filename.endswith(".json"):
            file_path = os.path.join(story_interactions_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if "story_activities_polls" in data or "story_activities_story_likes" in data:
                        story_activities = data.get("story_activities_polls", []) + data.get("story_activities_story_likes", [])
                        for activity in story_activities:
                            title = activity.get("title")
                            if title:
                                user_engagement[title] = user_engagement.get(title, 0) + 1
            except FileNotFoundError:
                raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
            except json.JSONDecodeError:
                raise ValueError("Error: Failed to decode JSON file.")

    return user_engagement

def write_csv(user_engagement):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, count in user_engagement.items():
            writer.writerow([user, count])

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        user_engagement = process_story_interactions(root_dir)
        write_csv(user_engagement)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()