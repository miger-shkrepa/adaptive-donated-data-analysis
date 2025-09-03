import os
import json
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_story_engagement_data():
    story_engagement = {}
    try:
        story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_path):
            story_likes_data = load_json_data(story_likes_path)
            for entry in story_likes_data["story_activities_story_likes"]:
                for data in entry["string_list_data"]:
                    user = entry["title"]
                    if user not in story_engagement:
                        story_engagement[user] = 0
                    story_engagement[user] += 1
        else:
            print("Warning: story_likes.json does not exist, treating its contribution as 0.")
    except Exception as e:
        print(f"Error processing story likes: {e}")

    return story_engagement

def write_to_csv(data):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, count in data.items():
            writer.writerow([user, count])

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    
    story_engagement_data = get_story_engagement_data()
    write_to_csv(story_engagement_data)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)