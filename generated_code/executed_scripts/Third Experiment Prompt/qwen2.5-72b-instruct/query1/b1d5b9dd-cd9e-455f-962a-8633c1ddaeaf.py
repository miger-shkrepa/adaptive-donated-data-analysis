import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        topics_of_interest = []

        # Construct the path to the recommended_topics.json file
        recommended_topics_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

        # Check if the file exists
        if not os.path.exists(recommended_topics_path):
            print("Warning: The recommended_topics.json file does not exist. Returning an empty list.")
            return topics_of_interest

        # Read the JSON file
        with open(recommended_topics_path, 'r') as file:
            data = json.load(file)

        # Extract the topics of interest
        for item in data.get("topics_your_topics", []):
            string_map_data = item.get("string_map_data", {})
            name = string_map_data.get("Name", {}).get("value")
            if name:
                topics_of_interest.append(name)

        return topics_of_interest

    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {str(e)}")

def write_to_csv(topics_of_interest):
    try:
        # Define the output file path
        output_file = 'query_responses/results.csv'

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Write the topics of interest to the CSV file
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])  # Write the header
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to CSV: {str(e)}")

# Main function to execute the script
def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest)
        print("CSV file has been created successfully.")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()