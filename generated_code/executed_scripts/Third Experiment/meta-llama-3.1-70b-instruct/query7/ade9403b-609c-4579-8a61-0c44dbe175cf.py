import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    user_engagement = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                if file_name == "story_likes.json":
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for story_like in data["story_activities_story_likes"]:
                            title = story_like["title"]
                            if title not in user_engagement:
                                user_engagement[title] = 0
                            user_engagement[title] += len(story_like["string_list_data"])
                elif file_name == "quizzes.json":
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for quiz in data["story_activities_quizzes"]:
                            title = quiz["title"]
                            if title not in user_engagement:
                                user_engagement[title] = 0
                            user_engagement[title] += len(quiz["string_list_data"])
        
        return user_engagement
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(user_engagement):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])
            for user, engagement in user_engagement.items():
                writer.writerow([user, engagement])
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        if not user_engagement:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["User", "Times Engaged"])
        else:
            write_to_csv(user_engagement)
    
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()