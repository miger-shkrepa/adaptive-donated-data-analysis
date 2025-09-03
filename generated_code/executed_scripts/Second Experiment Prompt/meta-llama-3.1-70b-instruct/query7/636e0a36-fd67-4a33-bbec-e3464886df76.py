import os
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store user engagement
        user_engagement = {}

        # Define the paths to the relevant files
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        story_reaction_sticker_reactions_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_reaction_sticker_reactions.json")
        emoji_story_reactions_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "emoji_story_reactions.json")
        polls_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "polls.json")
        quizzes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "quizzes.json")
        emoji_sliders_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "emoji_sliders.json")
        questions_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "questions.json")

        # Check if the required files exist
        required_files = [story_likes_path, story_reaction_sticker_reactions_path, emoji_story_reactions_path, polls_path, quizzes_path, emoji_sliders_path, questions_path]
        missing_files = [file for file in required_files if not os.path.exists(file)]

        if missing_files:
            # If any required files are missing, return a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['User', 'Times Engaged']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        # Load the data from the JSON files
        for file_path in required_files:
            with open(file_path, 'r') as file:
                data = eval(file.read())
                for item in data:
                    if 'title' in item:
                        user = item['title']
                        if user not in user_engagement:
                            user_engagement[user] = 0
                        user_engagement[user] += len(item.get('string_list_data', []))

        # Sort the user engagement dictionary by value in descending order
        sorted_user_engagement = sorted(user_engagement.items(), key=lambda x: x[1], reverse=True)

        # Write the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, engagement in sorted_user_engagement:
                writer.writerow({'User': user, 'Times Engaged': engagement})

    except Exception as e:
        raise ValueError("Error: " + str(e))

get_user_engagement(root_dir)