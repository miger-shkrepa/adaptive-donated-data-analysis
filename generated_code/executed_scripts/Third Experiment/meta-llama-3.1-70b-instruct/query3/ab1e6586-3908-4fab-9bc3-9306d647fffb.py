import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_post_views(root_dir):
    post_views = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                if file_name == "story_likes.json":
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        with open(file_path, 'r') as file:
                            data = eval(file.read())
                            for activity in data["story_activities_story_likes"]:
                                for timestamp_data in activity["string_list_data"]:
                                    timestamp = timestamp_data["timestamp"]
                                    date = datetime.fromtimestamp(timestamp).date()
                                    week = date.isocalendar()[0:2]
                                    week_str = f"Week {week[0]}-{week[1]:02d}"
                                    date_str = date.strftime("%Y-%m-%d")
                                    if date_str not in post_views:
                                        post_views[date_str] = 0
                                    if week_str not in post_views:
                                        post_views[week_str] = 0
                                    post_views[date_str] += 1
                                    post_views[week_str] += 1
                    except Exception as e:
                        raise ValueError(f"ValueError: Failed to parse {file_path}. {str(e)}")
        
        daily_views = [(date, views, "Daily") for date, views in post_views.items() if len(date) == 10]
        weekly_views = [(week, views, "Weekly") for week, views in post_views.items() if len(week) > 10]
        return daily_views + weekly_views
    
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(data, file_path):
    try:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            writer.writerows(data)
    except Exception as e:
        raise Exception(f"Error: Failed to save data to {file_path}. {str(e)}")

def main():
    try:
        data = get_post_views(root_dir)
        if not data:
            data = []
        save_to_csv(data, 'query_responses/results.csv')
    except Exception as e:
        print(f"Error: {str(e)}")
        save_to_csv([["Date/Week", "Posts Viewed", "Type"]], 'query_responses/results.csv')

if __name__ == "__main__":
    main()