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

        # Check if the 'your_instagram_activity' directory exists
        your_instagram_activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(your_instagram_activity_dir):
            # Check if the 'story_interactions' directory exists
            story_interactions_dir = os.path.join(your_instagram_activity_dir, 'story_interactions')
            if os.path.exists(story_interactions_dir):
                # Iterate over the story interaction files
                for filename in os.listdir(story_interactions_dir):
                    if filename.endswith('.json'):
                        # Open the JSON file
                        filepath = os.path.join(story_interactions_dir, filename)
                        with open(filepath, 'r') as file:
                            # Read the JSON file
                            import json
                            data = json.load(file)

                            # Iterate over the story interactions
                            for interaction in data.get('story_activities_emoji_sliders', []) + \
                                            data.get('story_activities_emoji_quick_reactions', []) + \
                                            data.get('story_activities_polls', []) + \
                                            data.get('story_activities_questions', []) + \
                                            data.get('story_activities_quizzes', []) + \
                                            data.get('story_activities_story_likes', []) + \
                                            data.get('story_activities_reaction_sticker_reactions', []):
                                # Get the user who posted the story
                                user = interaction.get('title')

                                # Increment the user's engagement count
                                if user in user_engagement:
                                    user_engagement[user] += 1
                                else:
                                    user_engagement[user] = 1

        # Create a CSV file with the user engagement data
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write the user engagement data
            for user, engagement in user_engagement.items():
                writer.writerow({'User': user, 'Times Engaged': engagement})

    except FileNotFoundError as e:
        # Create a CSV file with only the column headers if a required file does not exist
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise e

    except Exception as e:
        raise ValueError("Error: " + str(e))

get_user_engagement(root_dir)