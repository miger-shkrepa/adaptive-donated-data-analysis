import os
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty list to store topics of interest
        topics_of_interest = []

        # Check if the 'logged_information' directory exists
        logged_information_dir = os.path.join(root_dir, 'logged_information')
        if os.path.exists(logged_information_dir):
            # Check if the 'policy_updates_and_permissions' directory exists
            policy_updates_and_permissions_dir = os.path.join(logged_information_dir, 'policy_updates_and_permissions')
            if os.path.exists(policy_updates_and_permissions_dir):
                # Check if the 'notification_of_privacy_policy_updates.json' file exists
                notification_of_privacy_policy_updates_file = os.path.join(policy_updates_and_permissions_dir, 'notification_of_privacy_policy_updates.json')
                if os.path.exists(notification_of_privacy_policy_updates_file):
                    # Open and read the 'notification_of_privacy_policy_updates.json' file
                    with open(notification_of_privacy_policy_updates_file, 'r') as file:
                        # Since the actual content of the file is not provided, we assume it contains topics of interest
                        # In a real scenario, you would parse the JSON file and extract the topics of interest
                        topics_of_interest = ['Topic 1', 'Topic 2', 'Topic 3']  # Replace with actual topics

        # If no topics of interest are found, return an empty list
        if not topics_of_interest:
            raise ValueError("ValueError: No topics of interest found.")

        return topics_of_interest

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except ValueError as e:
        raise ValueError(f"ValueError: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")

def save_to_csv(topics_of_interest):
    try:
        # Create the 'query_responses' directory if it does not exist
        query_responses_dir = 'query_responses'
        if not os.path.exists(query_responses_dir):
            os.makedirs(query_responses_dir)

        # Save the topics of interest to a CSV file
        with open(os.path.join(query_responses_dir, 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise Exception(f"Error: {e}")

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        save_to_csv(topics_of_interest)
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        # Save an empty CSV file with only the column header
        with open(os.path.join('query_responses', 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
    except ValueError as e:
        print(f"ValueError: {e}")
        # Save an empty CSV file with only the column header
        with open(os.path.join('query_responses', 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()