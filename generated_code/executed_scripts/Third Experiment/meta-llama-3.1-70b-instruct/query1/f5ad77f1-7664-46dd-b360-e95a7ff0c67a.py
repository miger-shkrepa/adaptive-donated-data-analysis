import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty list to store topics of interest
        topics_of_interest = []

        # Define the path to the 'your_topics' directory
        your_topics_dir = os.path.join(root_dir, "preferences", "your_topics")

        # Check if the 'your_topics' directory exists
        if os.path.exists(your_topics_dir):
            # Define the path to the 'recommended_topics.json' file
            recommended_topics_file = os.path.join(your_topics_dir, "recommended_topics.json")

            # Check if the 'recommended_topics.json' file exists
            if os.path.exists(recommended_topics_file):
                # Open and load the 'recommended_topics.json' file
                with open(recommended_topics_file, "r") as file:
                    data = json.load(file)

                # Extract topics of interest from the 'recommended_topics.json' file
                for topic in data["topics_your_topics"]:
                    topics_of_interest.append(topic["string_map_data"]["Name"]["value"])

        # Return the list of topics of interest
        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_file = "query_responses/results.csv"

        # Create the 'query_responses' directory if it does not exist
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the topics of interest to the output CSV file
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the topics of interest
        topics_of_interest = get_topics_of_interest(root_dir)

        # Save the topics of interest to a CSV file
        save_topics_to_csv(topics_of_interest)

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except ValueError as e:
        raise ValueError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()