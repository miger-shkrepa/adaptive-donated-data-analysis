import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize lists to store the data
company_names = []
num_ads_viewed = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if "ads_information" in data and "ads_and_topics" in data["ads_information"]:
                # Iterate over the ads and topics
                for topic in data["ads_information"]["ads_and_topics"].values():
                    # Check if the topic has a title
                    if "title" in topic["structure"][0]:
                        # Get the company name and number of ads viewed
                        company_name = topic["structure"][0]["title"]
                        num_ads_viewed.append(1)

                        # Add the company name to the list
                        if company_name not in company_names:
                            company_names.append(company_name)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for i in range(len(company_names)):
        writer.writerow([company_names[i], num_ads_viewed[i]])