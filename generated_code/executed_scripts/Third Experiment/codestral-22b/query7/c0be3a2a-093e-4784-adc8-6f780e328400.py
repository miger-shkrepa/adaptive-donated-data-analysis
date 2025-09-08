import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

engagement_count = {}

# Iterate over all story folders
for story_folder in os.listdir(root_dir):
    story_path = os.path.join(root_dir, story_folder)

    if os.path.isdir(story_path):
        # Check for story_likes.json
        story_likes_path = os.path.join(story_path, "story_likes.json")
        if os.path.exists(story_likes_path):
            with open(story_likes_path, 'r') as f:
                data = json.load(f)
                for story in data["story_activities_story_likes"]:
                    if story["title"] in engagement_count:
                        engagement_count[story["title"]] += len(story["string_list_data"])
                    else:
                        engagement_count[story["title"]] = len(story["string_list_data"])

        # Check for questions.json
        questions_path = os.path.join(story_path, "questions.json")
        if os.path.exists(questions_path):
            with open(questions_path, 'r') as f:
                data = json.load(f)
                for story in data["story_activities_questions"]:
                    if story["title"] in engagement_count:
                        engagement_count[story["title"]] += len(story["string_list_data"])
                    else:
                        engagement_count[story["title"]] = len(story["string_list_data"])

        # Check for polls.json
        polls_path = os.path.join(story_path, "polls.json")
        if os.path.exists(polls_path):
            with open(polls_path, 'r') as f:
                data = json.load(f)
                for story in data["story_activities_polls"]:
                    if story["title"] in engagement_count:
                        engagement_count[story["title"]] += len(story["string_list_data"])
                    else:
                        engagement_count[story["title"]] = len(story["string_list_data"])

        # Check for quizzes.json
        quizzes_path = os.path.join(story_path, "quizzes.json")
        if os.path.exists(quizzes_path):
            with open(quizzes_path, 'r') as f:
                data = json.load(f)
                for story in data["story_activities_quizzes"]:
                    if story["title"] in engagement_count:
                        engagement_count[story["title"]] += len(story["string_list_data"])
                    else:
                        engagement_count[story["title"]] = len(story["string_list_data"])

# Write results to CSV
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, count in engagement_count.items():
        writer.writerow([user, count])