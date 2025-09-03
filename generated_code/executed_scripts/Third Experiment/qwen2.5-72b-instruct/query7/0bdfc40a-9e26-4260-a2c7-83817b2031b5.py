import os
import json
import csv

root_dir = "root_dir"

def get_story_engagement(root_dir):
    user_engagement = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_interactions_path = os.path.join(root_dir, "story_interactions")
        if not os.path.exists(story_interactions_path):
            return user_engagement

        for file_name in os.listdir(story_interactions_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(story_interactions_path, file_name)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    story_activities_key = list(data.keys())[0]
                    for activity in data[story_activities_key]:
                        title = activity.get("title", "")
                        if title:
                            user_engagement[title] = user_engagement.get(title, 0) + len(activity.get("string_list_data", []))

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decode error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

    return user_engagement

def save_to_csv(user_engagement):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, engagement in user_engagement.items():
            writer.writerow({'User': user, 'Times Engaged': engagement})

try:
    user_engagement = get_story_engagement(root_dir)
    save_to_csv(user_engagement)
except Exception as e:
    print(e)