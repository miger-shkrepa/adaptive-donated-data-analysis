import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    """
    This function calculates the user engagement based on the story interactions.
    
    Args:
    root_dir (str): The path to the root directory containing the user data.
    
    Returns:
    A dictionary where the keys are the user names and the values are the number of times the user has been engaged with.
    """
    
    # Initialize an empty dictionary to store the user engagement
    user_engagement = {}
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Define the story interaction sections
    story_interaction_sections = [
        "story_activities_emoji_sliders",
        "story_activities_emoji_quick_reactions",
        "story_activities_polls",
        "story_activities_questions",
        "story_activities_quizzes",
        "story_activities_story_likes",
        "story_activities_reaction_sticker_reactions"
    ]
    
    # Iterate over all json files in the story_interactions directory
    story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")
    if os.path.exists(story_interactions_dir):
        for filename in os.listdir(story_interactions_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(story_interactions_dir, filename)
                try:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for section in story_interaction_sections:
                            if section in data:
                                for item in data[section]:
                                    user = item["title"]
                                    engagement = len(item.get("string_list_data", []))
                                    if user in user_engagement:
                                        user_engagement[user] += engagement
                                    else:
                                        user_engagement[user] = engagement
                except json.JSONDecodeError:
                    raise ValueError("Error: The file {} is not a valid JSON file.".format(filename))
    else:
        # If the story_interactions directory does not exist, return an empty dictionary
        pass
    
    return user_engagement

def save_to_csv(user_engagement):
    """
    This function saves the user engagement to a CSV file.
    
    Args:
    user_engagement (dict): A dictionary where the keys are the user names and the values are the number of times the user has been engaged with.
    """
    
    # Define the CSV file path
    csv_file_path = "query_responses/results.csv"
    
    # Create the query_responses directory if it does not exist
    query_responses_dir = os.path.dirname(csv_file_path)
    if not os.path.exists(query_responses_dir):
        os.makedirs(query_responses_dir)
    
    # Save the user engagement to the CSV file
    with open(csv_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Times Engaged"])
        for user, engagement in user_engagement.items():
            writer.writerow([user, engagement])

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        save_to_csv(user_engagement)
    except Exception as e:
        # If an error occurs, save an empty CSV file with only the column headers
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])
        raise e

if __name__ == "__main__":
    main()