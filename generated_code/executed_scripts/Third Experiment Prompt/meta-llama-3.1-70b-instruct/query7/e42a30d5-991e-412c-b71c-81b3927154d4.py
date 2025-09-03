import os
import json
import csv

root_dir = "root_dir"

def get_engagement_data(root_dir):
    engagement_data = {}
    try:
        messages_dir = os.path.join(root_dir, "your_activity_across_facebook", "messages")
        for dir_name in os.listdir(messages_dir):
            if dir_name == "inbox":
                continue
            dir_path = os.path.join(messages_dir, dir_name)
            for file_name in os.listdir(dir_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for message in data["messages"]:
                            if "sender_name" in message:
                                sender_name = message["sender_name"]
                                if sender_name not in engagement_data:
                                    engagement_data[sender_name] = 0
                                engagement_data[sender_name] += 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))
    return engagement_data

def write_csv(engagement_data):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, times_engaged in engagement_data.items():
            writer.writerow([user, times_engaged])

def main():
    engagement_data = get_engagement_data(root_dir)
    if not engagement_data:
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
    else:
        write_csv(engagement_data)

if __name__ == "__main__":
    main()