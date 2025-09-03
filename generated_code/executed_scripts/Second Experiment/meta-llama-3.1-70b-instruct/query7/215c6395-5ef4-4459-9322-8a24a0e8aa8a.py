import os
import csv

root_dir = "root_dir"

def get_engagement_data(root_dir):
    engagement_data = {}
    try:
        messages_dir = os.path.join(root_dir, "messages", "inbox")
        if not os.path.exists(messages_dir):
            raise FileNotFoundError("FileNotFoundError: The messages directory does not exist.")
        
        for username in os.listdir(messages_dir):
            username_path = os.path.join(messages_dir, username)
            if not os.path.isdir(username_path):
                continue
            
            engagement_count = 0
            for filename in os.listdir(username_path):
                if filename.endswith(".json"):
                    file_path = os.path.join(username_path, filename)
                    try:
                        with open(file_path, "r") as file:
                            # Assuming the JSON file has a similar structure to the one in the context
                            # and that the reactions are the engagement data we're looking for
                            data = eval(file.read())
                            for message in data.get("messages", []):
                                if "reactions" in message:
                                    engagement_count += len(message["reactions"])
                    except Exception as e:
                        raise ValueError("Error: Failed to parse JSON file: " + str(e))
            
            engagement_data[username] = engagement_count
    
    except Exception as e:
        raise ValueError("Error: " + str(e))
    
    return engagement_data

def write_csv(engagement_data):
    try:
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["User", "Times Engaged"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, engagement in engagement_data.items():
                writer.writerow({"User": user, "Times Engaged": engagement})
    except Exception as e:
        raise ValueError("Error: Failed to write CSV file: " + str(e))

def main():
    try:
        engagement_data = get_engagement_data(root_dir)
        write_csv(engagement_data)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        if "messages directory does not exist" in str(e):
            with open("query_responses/results.csv", "w", newline="") as csvfile:
                fieldnames = ["User", "Times Engaged"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        else:
            raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()