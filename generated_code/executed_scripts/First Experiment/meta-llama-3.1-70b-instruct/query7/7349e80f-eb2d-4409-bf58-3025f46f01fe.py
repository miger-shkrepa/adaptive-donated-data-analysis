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
                            if title not in user_engagement:
                                user_engagement[title] = 0
                            user_engagement[title] += len(activity.get("string_list_data", []))

        # Iterate over the threads directory
        threads_dir = os.path.join(root_dir, "threads")
        if os.path.exists(threads_dir):
            for thread_dir in os.listdir(threads_dir):
                thread_path = os.path.join(threads_dir, thread_dir)
                if os.path.isdir(thread_path):
                    for filename in os.listdir(thread_path):
                        if filename.endswith(".json"):
                            file_path = os.path.join(thread_path, filename)
                            with open(file_path, "r") as file:
                                data = json.load(file)
                                participants = data.get("participants", [])
                                for participant in participants:
                                    name = participant.get("name")
                                    if name not in user_engagement:
                                        user_engagement[name] = 0
                                    user_engagement[name] += len(data.get("messages", []))

        # Sort the user engagement dictionary by value in descending order
        sorted_user_engagement = sorted(user_engagement.items(), key=lambda x: x[1], reverse=True)

        # Write the result to a CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
            for user, engagement in sorted_user_engagement:
                writer.writerow([user, engagement])

    except Exception as e:
        raise ValueError("ValueError: " + str(e))

get_user_engagement(root_dir)