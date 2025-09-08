import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the result dictionary
result = {"User": [], "Post Likes": [], "Story Likes": [], "Comments": []}

# Define the function to process the data
def process_data(root_dir):
    # Iterate over the subdirectories
    for dir in os.listdir(root_dir):
        # Check if the subdirectory is a JSON file
        if dir.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(root_dir, dir), "r") as f:
                # Load the JSON data
                data = json.load(f)

                # Process the data
                process_json(data, result)

# Define the function to process a JSON object
def process_json(data, result):
    # Check if the JSON object has the required structure
    if "likes" in data and "media_likes" in data["likes"]:
        # Process the media likes
        process_media_likes(data["likes"]["media_likes"], result)

    if "likes" in data and "comment_likes" in data["likes"]:
        # Process the comment likes
        process_comment_likes(data["likes"]["comment_likes"], result)

    if "story_activities" in data and "story_likes" in data["story_activities"]:
        # Process the story likes
        process_story_likes(data["story_activities"]["story_likes"], result)

    if "story_activities" in data and "questions" in data["story_activities"]:
        # Process the questions
        process_questions(data["story_activities"]["questions"], result)

    if "story_activities" in data and "quizzes" in data["story_activities"]:
        # Process the quizzes
        process_quizzes(data["story_activities"]["quizzes"], result)

    if "story_activities" in data and "polls" in data["story_activities"]:
        # Process the polls
        process_polls(data["story_activities"]["polls"], result)

    if "story_activities" in data and "emoji_sliders" in data["story_activities"]:
        # Process the emoji sliders
        process_emoji_sliders(data["story_activities"]["emoji_sliders"], result)

# Define the function to process media likes
def process_media_likes(media_likes, result):
    # Iterate over the media likes
    for like in media_likes:
        # Get the user and post likes
        user = like["title"]
        post_likes = len(like["string_list_data"])

        # Add the user and post likes to the result dictionary
        result["User"].append(user)
        result["Post Likes"].append(post_likes)

# Define the function to process comment likes
def process_comment_likes(comment_likes, result):
    # Iterate over the comment likes
    for like in comment_likes:
        # Get the user and comment likes
        user = like["title"]
        comment_likes = len(like["string_list_data"])

        # Add the user and comment likes to the result dictionary
        result["User"].append(user)
        result["Comments"].append(comment_likes)

# Define the function to process story likes
def process_story_likes(story_likes, result):
    # Iterate over the story likes
    for like in story_likes:
        # Get the user and story likes
        user = like["title"]
        story_likes = len(like["string_list_data"])

        # Add the user and story likes to the result dictionary
        result["User"].append(user)
        result["Story Likes"].append(story_likes)

# Define the function to process questions
def process_questions(questions, result):
    # Iterate over the questions
    for question in questions:
        # Get the user and question likes
        user = question["title"]
        question_likes = len(question["string_list_data"])

        # Add the user and question likes to the result dictionary
        result["User"].append(user)
        result["Comments"].append(question_likes)

# Define the function to process quizzes
def process_quizzes(quizzes, result):
    # Iterate over the quizzes
    for quiz in quizzes:
        # Get the user and quiz likes
        user = quiz["title"]
        quiz_likes = len(quiz["string_list_data"])

        # Add the user and quiz likes to the result dictionary
        result["User"].append(user)
        result["Comments"].append(quiz_likes)

# Define the function to process polls
def process_polls(polls, result):
    # Iterate over the polls
    for poll in polls:
        # Get the user and poll likes
        user = poll["title"]
        poll_likes = len(poll["string_list_data"])

        # Add the user and poll likes to the result dictionary
        result["User"].append(user)
        result["Comments"].append(poll_likes)

# Define the function to process emoji sliders
def process_emoji_sliders(emoji_sliders, result):
    # Iterate over the emoji sliders
    for slider in emoji_sliders:
        # Get the user and emoji slider likes
        user = slider["title"]
        emoji_slider_likes = len(slider["string_list_data"])

        # Add the user and emoji slider likes to the result dictionary
        result["User"].append(user)
        result["Comments"].append(emoji_slider_likes)

# Process the data
process_data(root_dir)

# Sort the result dictionary by user and then by likes
result["User"] = sorted(set(result["User"]))
result["Post Likes"] = sorted(result["Post Likes"], reverse=True)
result["Story Likes"] = sorted(result["Story Likes"], reverse=True)
result["Comments"] = sorted(result["Comments"], reverse=True)

# Write the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result["User"]))):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])