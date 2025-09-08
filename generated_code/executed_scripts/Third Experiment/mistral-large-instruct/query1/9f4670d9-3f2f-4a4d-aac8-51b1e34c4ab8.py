import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract topics of interest
def extract_topics_of_interest(root_dir):
    topics_of_interest = []

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Define the path to the JSON file containing topics of interest
    topics_file_path = os.path.join(root_dir, "logged_information", "policy_updates_and_permissions", "notification_of_privacy_policy_updates.json")

    # Check if the topics file exists
    if not os.path.exists(topics_file_path):
        raise FileNotFoundError("Error: The topics of interest file does not exist.")

    # Read the JSON file
    try:
        with open(topics_file_path, 'r') as file:
            data = json.load(file)
            for item in data.get("policy_updates_and_permissions_notification_of_privacy_policy_updates", []):
                string_map_data = item.get("string_map_data", {})
                consent_status = string_map_data.get("Consent Status", {}).get("value", "")
                if consent_status:
                    topics_of_interest.append(consent_status)
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from the topics of interest file.")

    return topics_of_interest

# Function to save the results to a CSV file
def save_to_csv(topics_of_interest):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

# Main function to execute the script
def main():
    try:
        topics_of_interest = extract_topics_of_interest(root_dir)
        save_to_csv(topics_of_interest)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()