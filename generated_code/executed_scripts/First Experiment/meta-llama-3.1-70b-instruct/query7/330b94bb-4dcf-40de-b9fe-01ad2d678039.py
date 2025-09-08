import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store user engagement
        user_engagement = {}

        # Iterate over all files in the root directory
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                # Check if the file is a JSON file
                if file_name.endswith(".json"):
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        # Open and load the JSON file
                        with open(file_path, 'r') as file:
                            data = json.load(file)

                        # Check if the file contains story interactions
                        if "story_activities" in data:
                            # Get the user who posted the story
                            user = data.get("title", "")

                            # Increment the engagement count for the user
                            if user in user_engagement:
                                user_engagement[user] += 1
                            else:
                                user_engagement[user] = 1

                    except json.JSONDecodeError:
                        raise ValueError("ValueError: Invalid JSON file.")

        return user_engagement

    except Exception as e:
        raise Exception("Error: " + str(e))

def save_to_csv(user_engagement):
    try:
        # Save the user engagement to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Times Engaged"])
            for user, engagement in user_engagement.items():
                writer.writerow([user, engagement])

    except Exception as e:
        raise Exception("Error: " + str(e))

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        save_to_csv(user_engagement)

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except ValueError as e:
        raise ValueError("ValueError: " + str(e))
    except Exception as e:
        raise Exception("Error: " + str(e))

if __name__ == "__main__":
    main()