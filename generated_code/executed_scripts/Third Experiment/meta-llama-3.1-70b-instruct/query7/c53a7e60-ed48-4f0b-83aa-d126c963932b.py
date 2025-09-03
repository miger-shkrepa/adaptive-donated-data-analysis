import os
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store user engagement
        user_engagement = {}

        # Iterate over the media directory
        media_dir = os.path.join(root_dir, "media")
        if os.path.exists(media_dir):
            stories_dir = os.path.join(media_dir, "stories")
            if os.path.exists(stories_dir):
                for date_dir in os.listdir(stories_dir):
                    date_dir_path = os.path.join(stories_dir, date_dir)
                    if os.path.isdir(date_dir_path):
                        for file in os.listdir(date_dir_path):
                            file_path = os.path.join(date_dir_path, file)
                            if os.path.isfile(file_path):
                                # Assuming the file name contains the user name
                                user = file.split("_")[0]
                                if user not in user_engagement:
                                    user_engagement[user] = 1
                                else:
                                    user_engagement[user] += 1

        return user_engagement

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(user_engagement):
    try:
        # Write the user engagement to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user, engagement in user_engagement.items():
                writer.writerow({'User': user, 'Times Engaged': engagement})

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        if user_engagement:
            write_to_csv(user_engagement)
        else:
            # If no user engagement data is found, write a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['User', 'Times Engaged']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()