import os
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    user_engagement = {}
    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".json") and "stories" in dirpath:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r') as file:
                            # Assuming the JSON file contains the story data
                            # Since the actual JSON structure is not provided, 
                            # we'll assume it's a simple JSON with the story data
                            story_data = eval(file.read())
                            for story in story_data.get("stories", []):
                                user = story.get("sender_name")
                                if user not in user_engagement:
                                    user_engagement[user] = 1
                                else:
                                    user_engagement[user] += 1
                    except Exception as e:
                        raise ValueError("Error: Failed to parse JSON file: " + str(e))
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: Failed to process directory: " + str(e))
    return user_engagement

def write_to_csv(user_engagement):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, engagement in user_engagement.items():
                writer.writerow({'User': user, 'Times Engaged': engagement})
    except Exception as e:
        raise ValueError("Error: Failed to write to CSV file: " + str(e))

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        if not user_engagement:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['User', 'Times Engaged']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        else:
            write_to_csv(user_engagement)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()