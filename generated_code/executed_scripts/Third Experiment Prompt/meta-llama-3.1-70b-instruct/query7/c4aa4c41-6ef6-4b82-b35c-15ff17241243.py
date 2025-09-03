import os
import json
import csv

root_dir = "root_dir"

def get_story_engagement(root_dir):
    story_engagement = {}
    try:
        # Navigate to the story_interactions directory
        story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")
        if not os.path.exists(story_interactions_dir):
            raise FileNotFoundError("Error: The story_interactions directory does not exist.")

        # Open the story_likes.json file
        story_likes_file = os.path.join(story_interactions_dir, "story_likes.json")
        if not os.path.exists(story_likes_file):
            raise FileNotFoundError("Error: The story_likes.json file does not exist.")

        with open(story_likes_file, "r") as file:
            story_likes_data = json.load(file)

        # Iterate over the story likes data
        for story_like in story_likes_data["story_activities_story_likes"]:
            title = story_like["title"]
            if title not in story_engagement:
                story_engagement[title] = 0
            story_engagement[title] += len(story_like["string_list_data"])

        # Open the polls.json file
        polls_file = os.path.join(story_interactions_dir, "polls.json")
        if os.path.exists(polls_file):
            with open(polls_file, "r") as file:
                polls_data = json.load(file)

            # Iterate over the polls data
            for poll in polls_data["story_activities_polls"]:
                title = poll["title"]
                if title not in story_engagement:
                    story_engagement[title] = 0
                story_engagement[title] += len(poll["string_list_data"])

        # Open the questions.json file
        questions_file = os.path.join(story_interactions_dir, "questions.json")
        if os.path.exists(questions_file):
            with open(questions_file, "r") as file:
                questions_data = json.load(file)

            # Iterate over the questions data
            for question in questions_data["story_activities_questions"]:
                title = question["title"]
                if title not in story_engagement:
                    story_engagement[title] = 0
                story_engagement[title] += len(question["string_list_data"])

    except FileNotFoundError as e:
        raise e

    return story_engagement

def write_to_csv(story_engagement):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Times Engaged"])
        for user, times_engaged in story_engagement.items():
            writer.writerow([user, times_engaged])

def main():
    try:
        story_engagement = get_story_engagement(root_dir)
        write_to_csv(story_engagement)
    except FileNotFoundError as e:
        print(e)
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])

if __name__ == "__main__":
    main()