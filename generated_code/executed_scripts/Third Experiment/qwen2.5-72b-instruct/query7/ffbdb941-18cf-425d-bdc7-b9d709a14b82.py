import os
import json
import csv

root_dir = "root_dir"

def process_story_engagement(root):
    user_engagement = {}
    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_likes_path = os.path.join(root, "stories", "story_likes.json")
        quizzes_path = os.path.join(root, "stories", "quizzes.json")
        questions_path = os.path.join(root, "stories", "questions.json")
        
        for path in [story_likes_path, quizzes_path, questions_path]:
            if os.path.exists(path):
                with open(path, 'r') as file:
                    data = json.load(file)
                    if "story_activities_story_likes" in data:
                        for item in data["story_activities_story_likes"]:
                            title = item.get("title", "")
                            user_engagement[title] = user_engagement.get(title, 0) + len(item.get("string_list_data", []))
                    if "story_activities_quizzes" in data:
                        for item in data["story_activities_quizzes"]:
                            title = item.get("title", "")
                            user_engagement[title] = user_engagement.get(title, 0) + len(item.get("string_list_data", []))
                    if "story_activities_questions" in data:
                        for item in data["story_activities_questions"]:
                            title = item.get("title", "")
                            user_engagement[title] = user_engagement.get(title, 0) + len(item.get("string_list_data", []))
            else:
                print(f"Warning: {path} does not exist. Skipping.")
        
        if not user_engagement:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["User", "Times Engaged"])
        else:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["User", "Times Engaged"])
                for user, engagement in user_engagement.items():
                    writer.writerow([user, engagement])
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding failed. Reason: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred. Reason: {str(e)}")

process_story_engagement(root_dir)