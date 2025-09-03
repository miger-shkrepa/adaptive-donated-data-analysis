import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store user engagement
        user_engagement = {}

        # Iterate over the story_sticker_interactions directory
        story_sticker_interactions_dir = os.path.join(root_dir, "story_sticker_interactions")
        if os.path.exists(story_sticker_interactions_dir):
            for filename in os.listdir(story_sticker_interactions_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(story_sticker_interactions_dir, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for activity in data.get("story_activities_emoji_sliders", []) + data.get("story_activities_polls", []) + data.get("story_activities_quizzes", []) + data.get("story_activities_questions", []) + data.get("story_activities_story_likes", []):
                            title = activity.get("title")
                            if title:
                                if title not in user_engagement:
                                    user_engagement[title] = 0
                                user_engagement[title] += len(activity.get("string_list_data", []))

        # Create a list of tuples containing the user and their engagement count
        user_engagement_list = [(user, count) for user, count in user_engagement.items()]

        # Sort the list in descending order based on the engagement count
        user_engagement_list.sort(key=lambda x: x[1], reverse=True)

        return user_engagement_list

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(data, filename):
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])
            for row in data:
                writer.writerow(row)
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        save_to_csv(user_engagement, "query_responses/results.csv")
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()