import os
import json
import csv

root_dir = "root_dir"

def process_story_interactions(root_dir):
    story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")

    if not os.path.exists(story_interactions_dir):
        raise FileNotFoundError("Error: The story interactions directory does not exist.")

    user_engagement = {}

    interaction_files = [
        "story_activities_emoji_sliders.json",
        "story_activities_emoji_quick_reactions.json",
        "story_activities_polls.json",
        "story_activities_questions.json",
        "story_activities_quizzes.json",
        "story_activities_story_likes.json",
        "story_activities_reaction_sticker_reactions.json"
    ]

    for file_name in interaction_files:
        file_path = os.path.join(story_interactions_dir, file_name)
        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                for entry in data:
                    user = entry.get("title", "")
                    if user:
                        string_list_data = entry.get("string_list_data", [])
                        times_engaged = len(string_list_data)
                        if user in user_engagement:
                            user_engagement[user] += times_engaged
                        else:
                            user_engagement[user] = times_engaged
        except json.JSONDecodeError:
            raise ValueError(f"Error: Invalid JSON format in file {file_path}.")
        except Exception as e:
            raise ValueError(f"Error: An error occurred while processing file {file_path}. {str(e)}")

    return user_engagement

def save_to_csv(user_engagement):
    output_dir = "query_responses"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "results.csv")

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["User", "Times Engaged"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, times_engaged in user_engagement.items():
            writer.writerow({"User": user, "Times Engaged": times_engaged})

if __name__ == "__main__":
    try:
        user_engagement = process_story_interactions(root_dir)
        save_to_csv(user_engagement)
    except Exception as e:
        print(e)