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
                                    user_engagement[title] = 1
                                else:
                                    user_engagement[title] += 1

        # Create a list of tuples to store user engagement
        user_engagement_list = [(user, times) for user, times in user_engagement.items()]

        # Sort the list in descending order based on times engaged
        user_engagement_list.sort(key=lambda x: x[1], reverse=True)

        return user_engagement_list

    except Exception as e:
        raise ValueError("ValueError: " + str(e))

def save_to_csv(user_engagement_list):
    try:
        # Create the results directory if it does not exist
        results_dir = "query_responses"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Save the user engagement list to a CSV file
        with open(os.path.join(results_dir, "results.csv"), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])
            for user, times in user_engagement_list:
                writer.writerow([user, times])

    except Exception as e:
        raise ValueError("ValueError: " + str(e))

def main():
    try:
        user_engagement_list = get_user_engagement(root_dir)
        save_to_csv(user_engagement_list)
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()