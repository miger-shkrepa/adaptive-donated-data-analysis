import os
import json
import csv

root_dir = "root_dir"

def process_json_files(directory):
    user_engagement = {}
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for section in [
                        "story_activities_emoji_sliders",
                        "story_activities_emoji_quick_reactions",
                        "story_activities_polls",
                        "story_activities_questions",
                        "story_activities_quizzes",
                        "story_activities_story_likes",
                        "story_activities_reaction_sticker_reactions"
                    ]:
                        if section in data:
                            for entry in data[section]:
                                user = entry.get("title", "")
                                times_engaged = len(entry.get("string_list_data", []))
                                if user:
                                    user_engagement[user] = user_engagement.get(user, 0) + times_engaged
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: JSON file is not properly formatted.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    return user_engagement

def save_to_csv(data, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
        for user, times_engaged in data.items():
            writer.writerow([user, times_engaged])

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")
        if not os.path.exists(story_interactions_dir):
            save_to_csv({}, 'query_responses/results.csv')
            return
        
        user_engagement = process_json_files(story_interactions_dir)
        save_to_csv(user_engagement, 'query_responses/results.csv')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()