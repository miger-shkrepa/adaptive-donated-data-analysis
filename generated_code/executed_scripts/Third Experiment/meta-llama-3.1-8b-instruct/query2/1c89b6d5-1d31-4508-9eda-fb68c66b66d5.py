import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize lists to store data
company_names = []
num_ads_viewed = []

# Iterate over the ads information
for company in os.listdir(root_dir):
    if company.startswith("instagram_ads_and_businesses"):
        company_path = os.path.join(root_dir, company)
        for file in os.listdir(company_path):
            if file == "ads_about_meta.json":
                with open(os.path.join(company_path, file), 'r') as f:
                    data = json.load(f)
                    for label in data["label_values"]:
                        company_names.append(label["label"])
                        num_ads_viewed.append(label["value"])

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for i in range(len(company_names)):
        writer.writerow([company_names[i], num_ads_viewed[i]])