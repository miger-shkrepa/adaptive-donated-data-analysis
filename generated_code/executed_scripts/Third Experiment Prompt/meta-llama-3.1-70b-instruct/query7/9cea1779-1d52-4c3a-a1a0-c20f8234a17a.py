import os
import json
import csv

root_dir = "root_dir"

def get_story_engagement(root_dir):
    story_engagement = {}
    try:
        for filename in os.listdir(os.path.join(root_dir, "your_instagram_activity", "story_interactions")):
            if filename == "story_likes.json":
                with open(os.path.join(root_dir, "your_instagram_activity", "story_interactions", filename), "r") as file:
                    data = json.load(file)
                    for item in data["story_activities_story_likes"]:
                        user = item["title"]
                        times_engaged = len(item["string_list_data"])
                        if user in story_engagement:
                            story_engagement[user] += times_engaged
                        else:
                            story_engagement[user] = times_engaged
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))
    return story_engagement

def write_to_csv(story_engagement):
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Times Engaged"])
        for user, times_engaged in story_engagement.items():
            writer.writerow([user, times_engaged])

def main():
    story_engagement = get_story_engagement(root_dir)
    if not story_engagement:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])
    else:
        write_to_csv(story_engagement)

if __name__ == "__main__":
    main()