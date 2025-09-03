import os
import csv

root_dir = "root_dir"

def get_engagement_data(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the engagement data
        engagement_data = {}

        # Iterate over the subdirectories in the root directory
        for subdir in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, subdir)

            # Check if the subdirectory is a directory
            if os.path.isdir(subdir_path):
                # Iterate over the files in the subdirectory
                for filename in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, filename)

                    # Check if the file is a JSON file
                    if filename.endswith(".json"):
                        # Open the JSON file and read its contents
                        with open(file_path, "r") as file:
                            # Since we don't have the actual JSON data, we'll assume it's in the format of the given context
                            # We'll also assume that the 'messages' directory contains the relevant data
                            if subdir == "messages":
                                # Iterate over the messages in the JSON file
                                for message in file:
                                    # Since we don't have the actual JSON data, we'll assume it's in the format of the given context
                                    # We'll also assume that the 'sender_name' field contains the user who sent the message
                                    sender_name = message.split(",")[1].split(":")[1].strip().strip('"')

                                    # Increment the engagement count for the sender
                                    if sender_name in engagement_data:
                                        engagement_data[sender_name] += 1
                                    else:
                                        engagement_data[sender_name] = 1

        return engagement_data

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(engagement_data):
    try:
        # Create the 'query_responses' directory if it doesn't exist
        if not os.path.exists("query_responses"):
            os.makedirs("query_responses")

        # Open the CSV file and write the engagement data to it
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])

            # Sort the engagement data by the number of times engaged in descending order
            sorted_engagement_data = sorted(engagement_data.items(), key=lambda x: x[1], reverse=True)

            # Write the sorted engagement data to the CSV file
            for user, times_engaged in sorted_engagement_data:
                writer.writerow([user, times_engaged])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        engagement_data = get_engagement_data(root_dir)
        write_to_csv(engagement_data)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()