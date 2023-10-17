import requests
import json
import os
import argparse

# Jira API URL to retrieve issue types
url = "https://jira.trimble.tools/rest/api/2/issuetype"

# Define a function to extract issues
def extract_issues(input_file, output_file, bearer_token):
    # Set the Bearer Token in the Authorization header
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    # Send a GET request to the Jira API with the Bearer Token
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        issue_types = response.json()

        # Create a dictionary to map issue type IDs to names
        number_mapping = {int(item["id"]): item["name"] for item in issue_types}

        def mapping_id_to_type(number):
            return number_mapping.get(int(number), "Unknown")

        # Load JSON data from file
        with open(input_file, 'r', encoding='utf-8') as file:
            extracted_values = json.load(file)

        extracted_issues = {}

        for key, issues_array in extracted_values['contents'].items():
            filtered_issues = []

            for issue in issues_array:

                if isinstance(issue, dict):
                    filtered_issue = {
                        'key': issue['key'],
                        'summary': issue['summary'],
                        'typeid': mapping_id_to_type(int(issue['typeId']))
                    }
                    filtered_issues.append(filtered_issue)

            sorted_issues = sorted(filtered_issues, key=lambda x: x['typeid'])
            extracted_issues[key] = sorted_issues

        # Write the extracted values to a new JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(extracted_issues, file)

        # Delete the input JSON file (if it exists)
        if os.path.exists(input_file):
            os.remove(input_file)

        print(f"Extracted values have been saved to {output_file}")

    else:
        print(f"Failed to retrieve issue types. Status code: {response.status_code}")


