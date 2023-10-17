import sys
from ExtractJson import extract_issues
from Api import hit_api_and_save_json, get_board_id_using_project_id, get_project_id_using_project_name, get_sprint_id
from JsonToPdf import json_to_pdf

#---------------------------------------------------------------------------------
#user input
#jira_url = 'https://jira.trimble.tools'
#auth_id = 'NDA4MjA3NzAyMTM3OjmqoonIC9KgK8Uxh6vxrE/bMfU5'
#project_name="TOTO"
#sprint_name= "November 2022, Week 2"

#----------------------------------------------------------------------------------    
def generate_release_notes(project_name, sprint_name, auth_id, releaseVersion, testType, instancesTested, platformOsVersion, apiVersion, releaseDate, releaseType):
    jira_url = 'https://jira.trimble.tools'
    headers = {
    'Authorization': f'Bearer {auth_id}',
    'Content-Type': 'application/json'
    }

    #Get board Id using Project name
    get_project_id_using_project_name(project_name, auth_id, jira_url)
    board_id = get_board_id_using_project_id(project_name, auth_id, jira_url,sprint_name)
    print(" Project Board ID:", board_id)

    #Get sprint id from sprint name u
    sprint_id = get_sprint_id(sprint_name, jira_url, auth_id, board_id)
    sprint_report_file = sprint_name +'_report.json'
    if sprint_id is not None:
        print(f"The ID of {sprint_name} is {sprint_id}.")
    else:
        print(f"{sprint_name} not found or unable to fetch the sprint details.")


    # Hit the API and save JSON
    api_endpoint = f'{jira_url}/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId={board_id}&sprintId={sprint_id}'
    hit_api_and_save_json(api_endpoint, headers, sprint_report_file)

    # Extract issues from JSON
    extracted_values_file = sprint_name +'_extracted_values.json'
    extract_issues(sprint_report_file, extracted_values_file,auth_id)

    # Convert JSON to PDF
    json_to_pdf(extracted_values_file,sprint_name,releaseVersion, testType, instancesTested, platformOsVersion, apiVersion, releaseDate, releaseType)

if __name__ == "__main__":
    if len(sys.argv) != 11:
        print("Usage: python main.py <projectName> <sprintName> <authId> <releaseVersion> <testType> <instancesTested> <platformOsVersion> <apiVersion> <releaseDate> <releaseType>")
        sys.exit(1)

    projectName = sys.argv[1]
    sprintName = sys.argv[2]
    authId = sys.argv[3]
    releaseVersion = sys.argv[4]
    testType = sys.argv[5]
    instancesTested = sys.argv[6]
    platformOsVersion = sys.argv[7]
    apiVersion = sys.argv[8]
    releaseDate = sys.argv[9]
    releaseType = sys.argv[10]

    generate_release_notes(projectName, sprintName, authId, releaseVersion, testType, instancesTested, platformOsVersion, apiVersion, releaseDate, releaseType)

