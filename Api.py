import requests
import json

def hit_api_and_save_json(api_endpoint, headers, output_file):
    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        sprint_report = response.json()
        with open(output_file, 'w') as file:
            json.dump(sprint_report, file)
        print(f"Sprint report saved to {output_file}")
    else:
        try:
            error_message = response.json()['errorMessages'][0]
            print(f"Error: {response.status_code} - {error_message}")
        except (json.JSONDecodeError, KeyError, IndexError):
            print(f"Error: {response.status_code} - {response.text}")


def get_project_id_using_project_name(project_name, oauth_access_token, jira_url):
    headers = {
        "Authorization": f"Bearer {oauth_access_token}",
        "Content-Type": "application/json"
    }

    # Get the Project ID
    project_api_url = f"{jira_url}/rest/api/2/project/{project_name}"
    response = requests.get(project_api_url, headers=headers)
    project_data = response.json()
    project_id = project_data["id"]
    return project_id

def get_board_id_using_project_id(project_id,oauth_access_token,jira_url,sprint_name):
    headers = {
        "Authorization": f"Bearer {oauth_access_token}",
        "Content-Type": "application/json"
    }
      
    # Retrieve the Board ID
    board_api_url = f"{jira_url}/rest/agile/1.0/board?projectKeyOrId={project_id}&type=scrum"
    response = requests.get(board_api_url, headers=headers)
    board_data = response.json()
    sprint_id = None

    for board in board_data["values"]:
        board_id = board["id"]
        
        # Use the second function to retrieve the sprint ID for the given sprint name
        sprint_id = get_sprint_id(sprint_name, jira_url, oauth_access_token, board_id)
        
        if sprint_id:
            # Sprint found in this board, break the loop and return the sprint ID
            break
   
    return board_id


def get_sprint_id(sprint_name, jira_base_url, jira_api_token, board_id):
    url = f"{jira_base_url}/rest/agile/1.0/board/{board_id}/sprint"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jira_api_token}"
    }
    start_at = 0
    max_results = 50  # Adjust the value below 50 if needed max is 50
    sprint_id = None

    while True:
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            sprints = response.json()["values"]
            for sprint in sprints:
                if sprint["name"].lower() == sprint_name.lower():
                    sprint_id = sprint["id"]
                    break

        if sprint_id is not None or len(sprints) < max_results:
            break

        start_at += max_results

    return sprint_id








