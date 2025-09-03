import os
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        user_engagement = {}

        # Iterate over all files in the directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "message_1.json":
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r') as file:
                            # Since we don't have the actual JSON data, we'll assume it's a simple JSON file
                            # with a list of messages, each containing a sender_name and reactions
                            messages = []
                            for line in file:
                                messages.append(eval(line))

                            for message in messages:
                                if 'sender_name' in message:
                                    sender_name = message['sender_name']
                                    if sender_name not in user_engagement:
                                        user_engagement[sender_name] = 0
                                    if 'reactions' in message:
                                        user_engagement[sender_name] += len(message['reactions'])
                    except Exception as e:
                        raise ValueError("Error: Failed to parse JSON file: " + str(e))

        return user_engagement

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(user_engagement):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user, engagement in user_engagement.items():
                writer.writerow({'User': user, 'Times Engaged': engagement})

    except Exception as e:
        raise ValueError("Error: Failed to save to CSV file: " + str(e))

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        save_to_csv(user_engagement)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()