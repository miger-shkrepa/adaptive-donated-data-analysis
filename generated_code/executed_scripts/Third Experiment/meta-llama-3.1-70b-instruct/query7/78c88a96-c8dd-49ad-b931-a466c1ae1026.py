import os
import csv

root_dir = "root_dir"

def get_story_engagements(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize dictionary to store story engagements
        story_engagements = {}

        # Iterate over directories in root directory
        for dir_name in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, dir_name)

            # Check if directory is 'story_interactions'
            if dir_name == 'story_interactions':
                # Iterate over files in 'story_interactions' directory
                for file_name in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file_name)

                    # Check if file is 'story_likes.json'
                    if file_name == 'story_likes.json':
                        try:
                            # Open and read 'story_likes.json' file
                            with open(file_path, 'r') as file:
                                # Iterate over story likes
                                for story_like in eval(file.read())['story_activities_story_likes']:
                                    # Get title of story
                                    title = story_like['title']

                                    # Increment engagement count for story
                                    if title in story_engagements:
                                        story_engagements[title] += len(story_like['string_list_data'])
                                    else:
                                        story_engagements[title] = len(story_like['string_list_data'])
                        except Exception as e:
                            raise ValueError("ValueError: Error parsing 'story_likes.json' file: " + str(e))

        return story_engagements

    except Exception as e:
        raise Exception("Error: " + str(e))

def write_to_csv(story_engagements):
    try:
        # Open and write to 'results.csv' file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])

            # Write story engagements to 'results.csv' file
            for user, engagements in story_engagements.items():
                writer.writerow([user, engagements])

    except Exception as e:
        raise Exception("Error: " + str(e))

def main():
    try:
        story_engagements = get_story_engagements(root_dir)

        # Check if story engagements are empty
        if not story_engagements:
            # Write empty 'results.csv' file with column headers
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["User", "Times Engaged"])
        else:
            write_to_csv(story_engagements)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()