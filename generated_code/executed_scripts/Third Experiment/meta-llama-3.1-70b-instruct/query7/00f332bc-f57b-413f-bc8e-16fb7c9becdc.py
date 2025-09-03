import os
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    user_engagement = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_interactions_dir = os.path.join(root_dir, "story_interactions")
        if not os.path.exists(story_interactions_dir):
            return user_engagement
        
        for filename in os.listdir(story_interactions_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(story_interactions_dir, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = eval(file.read())
                        for activity in data.get("story_activities_" + filename.split('.')[0], []):
                            title = activity.get("title")
                            if title not in user_engagement:
                                user_engagement[title] = 0
                            user_engagement[title] += len(activity.get("string_list_data", []))
                except Exception as e:
                    raise ValueError("Error: Failed to parse " + filename + ": " + str(e))
        
        return user_engagement
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

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
        write_to_csv(user_engagement)
    except Exception as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()