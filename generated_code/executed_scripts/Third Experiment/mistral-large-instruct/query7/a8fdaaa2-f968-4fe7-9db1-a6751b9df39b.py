import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to process the story_likes.json file
def process_story_likes(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            user_engagement = {}
            for story in data.get("story_activities_story_likes", []):
                title = story.get("title", "")
                timestamps = story.get("string_list_data", [])
                if title and timestamps:
                    if title not in user_engagement:
                        user_engagement[title] = 0
                    user_engagement[title] += len(timestamps)
            return user_engagement
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The story_likes.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The story_likes.json file is not a valid JSON.")

# Function to write the results to a CSV file
def write_to_csv(user_engagement):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, times_engaged in user_engagement.items():
                writer.writerow({'User': user, 'Times Engaged': times_engaged})
    except Exception as e:
        raise ValueError(f"ValueError: Failed to write to CSV file. {str(e)}")

# Main function to process the directory and generate the CSV file
def main():
    story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    if not os.path.exists(story_likes_path):
        # If the story_likes.json file does not exist, create a CSV with only the column headers
        write_to_csv({})
        return

    user_engagement = process_story_likes(story_likes_path)
    write_to_csv(user_engagement)

if __name__ == "__main__":
    main()