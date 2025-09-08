import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract story engagement data
def extract_story_engagement(root_dir):
    engagement_count = {}

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Traverse the directory structure
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "instagram_profile_information.json":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for item in data.get("profile_account_insights", []):
                            string_map_data = item.get("string_map_data", {})
                            for key, value in string_map_data.items():
                                if "Story Time" in key:
                                    user = value.get("value", "")
                                    if user:
                                        if user not in engagement_count:
                                            engagement_count[user] = 0
                                        engagement_count[user] += 1
                except json.JSONDecodeError:
                    raise ValueError("Error: Invalid JSON format in file {}".format(file_path))
                except Exception as e:
                    raise ValueError("Error: {}".format(str(e)))

    return engagement_count

# Function to save results to CSV
def save_to_csv(engagement_count):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, count in engagement_count.items():
            writer.writerow({'User': user, 'Times Engaged': count})

# Main function
def main():
    try:
        engagement_count = extract_story_engagement(root_dir)
        save_to_csv(engagement_count)
        print("Results saved to query_responses/results.csv")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()