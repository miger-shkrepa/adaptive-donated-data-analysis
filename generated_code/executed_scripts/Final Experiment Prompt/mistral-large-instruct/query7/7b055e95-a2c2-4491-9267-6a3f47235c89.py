import os
import json
import csv

root_dir = "root_dir"

def process_story_interactions(root_dir):
    story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")

    if not os.path.exists(story_interactions_dir):
        raise FileNotFoundError("Error: The story interactions directory does not exist.")

    user_engagement = {}

    for filename in os.listdir(story_interactions_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(story_interactions_dir, filename)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for key in data:
                        if isinstance(data[key], list):
                            for item in data[key]:
                                if "title" in item and "string_list_data" in item:
                                    user = item["title"]
                                    times_engaged = len(item["string_list_data"])
                                    if user in user_engagement:
                                        user_engagement[user] += times_engaged
                                    else:
                                        user_engagement[user] = times_engaged
            except json.JSONDecodeError:
                raise ValueError(f"Error: Invalid JSON format in file {file_path}.")
            except Exception as e:
                raise ValueError(f"Error: An error occurred while processing file {file_path}. {str(e)}")

    return user_engagement

def save_to_csv(user_engagement):
    output_dir = "query_responses"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "results.csv")

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["User", "Times Engaged"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, times_engaged in user_engagement.items():
            writer.writerow({"User": user, "Times Engaged": times_engaged})

def main():
    try:
        user_engagement = process_story_interactions(root_dir)
        save_to_csv(user_engagement)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()