import os
import json
import csv

root_dir = "root_dir"

def get_story_engagements(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the story engagements
        story_engagements = {}

        # Iterate over the story interactions
        story_interactions_dir = os.path.join(root_dir, "story_interactions")
        if os.path.exists(story_interactions_dir):
            for filename in os.listdir(story_interactions_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(story_interactions_dir, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for item in data.get("story_activities_story_likes", []) + data.get("story_activities_polls", []):
                            title = item.get("title")
                            if title:
                                if title not in story_engagements:
                                    story_engagements[title] = 0
                                story_engagements[title] += 1

        # Iterate over the saved posts
        saved_dir = os.path.join(root_dir, "saved")
        if os.path.exists(saved_dir):
            saved_posts_file = os.path.join(saved_dir, "saved_posts.json")
            if os.path.exists(saved_posts_file):
                with open(saved_posts_file, "r") as file:
                    data = json.load(file)
                    for item in data.get("saved_saved_media", []):
                        title = item.get("title")
                        if title:
                            if title not in story_engagements:
                                story_engagements[title] = 0
                            story_engagements[title] += 1

        return story_engagements

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(story_engagements):
    try:
        # Write the story engagements to a CSV file
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])
            for user, times_engaged in story_engagements.items():
                writer.writerow([user, times_engaged])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        story_engagements = get_story_engagements(root_dir)
        if story_engagements:
            write_to_csv(story_engagements)
        else:
            with open("query_responses/results.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["User", "Times Engaged"])

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()