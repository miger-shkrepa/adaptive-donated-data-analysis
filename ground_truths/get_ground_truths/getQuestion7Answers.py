import os
import json
import csv

def extract_user_engagement(base_folder):
    engagement_dir = os.path.join(base_folder, "your_instagram_activity", "story_interactions")
    user_engagement = {}

    if not os.path.exists(engagement_dir):
        print(f"Warning: story_interactions not found in {base_folder}. Skipping.")
        return None

    for filename in os.listdir(engagement_dir):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(engagement_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON decode error in {file_path}: {e}")
            continue

        keys = [
            "story_activities_reaction_sticker_reactions",
            "story_activities_emoji_quick_reactions",
            "story_activities_emoji_sliders",
            "story_activities_polls",
            "story_activities_quizzes",
            "story_activities_questions",
            "story_activities_story_likes",
        ]

        for key in keys:
            for activity in data.get(key, []):
                title = activity.get("title")
                if title:
                    user_engagement[title] = user_engagement.get(title, 0) + len(activity.get("string_list_data", []))

    return user_engagement

def save_user_engagement_to_csv(user_engagement, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, count in user_engagement.items():
            writer.writerow([user, count])
    print(f"✅ Saved: {output_file}")

def main():
    datasets_dir = "../../datasets"
    output_dir = os.path.join("../../ground_truths", "query7")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: Directory '{datasets_dir}' does not exist.")
        return

    for subdir in os.listdir(datasets_dir):
        full_path = os.path.join(datasets_dir, subdir)
        if not os.path.isdir(full_path):
            continue

        user_engagement = extract_user_engagement(full_path)

        if user_engagement is None:
            output_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")
            with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["User", "Times Engaged"])
            print(f"⚠️  No data file found. Created placeholder: {output_file}")
            continue

        if not user_engagement:
            continue

        output_file = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
        save_user_engagement_to_csv(user_engagement, output_file)

if __name__ == "__main__":
    main()
