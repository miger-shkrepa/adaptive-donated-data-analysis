import os
import json
import csv

root_dir = "root_dir"

def get_engagement_data(root_dir):
    engagement_data = {}
    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "story_likes.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for item in data['story_activities_story_likes']:
                            user = item['title']
                            if user not in engagement_data:
                                engagement_data[user] = 0
                            engagement_data[user] += len(item['string_list_data'])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    return engagement_data

def write_csv(engagement_data):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, times_engaged in engagement_data.items():
            writer.writerow({'User': user, 'Times Engaged': times_engaged})

def main():
    engagement_data = get_engagement_data(root_dir)
    write_csv(engagement_data)

if __name__ == "__main__":
    main()