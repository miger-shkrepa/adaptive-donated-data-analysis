import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    user_engagement = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_interactions_dir = os.path.join(root_dir, "story_interactions")
        if not os.path.exists(story_interactions_dir):
            return user_engagement
        
        story_likes_file = os.path.join(story_interactions_dir, "story_likes.json")
        if not os.path.exists(story_likes_file):
            return user_engagement
        
        with open(story_likes_file, 'r') as file:
            story_likes_data = json.load(file)
            for story_like in story_likes_data["story_activities_story_likes"]:
                title = story_like["title"]
                string_list_data = story_like["string_list_data"]
                for data in string_list_data:
                    if title not in user_engagement:
                        user_engagement[title] = 1
                    else:
                        user_engagement[title] += 1
        
        polls_file = os.path.join(story_interactions_dir, "polls.json")
        if os.path.exists(polls_file):
            with open(polls_file, 'r') as file:
                polls_data = json.load(file)
                for poll in polls_data["story_activities_polls"]:
                    title = poll["title"]
                    string_list_data = poll["string_list_data"]
                    for data in string_list_data:
                        if title not in user_engagement:
                            user_engagement[title] = 1
                        else:
                            user_engagement[title] += 1
        
        questions_file = os.path.join(story_interactions_dir, "questions.json")
        if os.path.exists(questions_file):
            with open(questions_file, 'r') as file:
                questions_data = json.load(file)
                for question in questions_data["story_activities_questions"]:
                    title = question["title"]
                    string_list_data = question["string_list_data"]
                    for data in string_list_data:
                        if title not in user_engagement:
                            user_engagement[title] = 1
                        else:
                            user_engagement[title] += 1
        
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
    user_engagement = get_user_engagement(root_dir)
    if not user_engagement:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])
    else:
        write_to_csv(user_engagement)

if __name__ == "__main__":
    main()