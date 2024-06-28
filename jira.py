import os
import argparse
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from atlassian import Jira
from github_scanning import scan_for_dependabot_alerts_and_issues
from repos import list_repos_in_org
from date_time import date_time
from common_utils import limit_string_length, compare_summaries_from_epic_and_scan


# Function to create a story under a specific epic
def create_story_under_epic(epic_key: str, summary: str, description: str):
    """
    Create jira task under a specific epic
    :param epic_key:
    :param summary:
    :param description:
    :return:
    """
    # Initializing jira client
    load_dotenv()
    JIRA_URL = os.getenv('JIRA_URL')
    JIRA_USERNAME = os.getenv('JIRA_USERNAME')
    JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
    jira = Jira(url=os.getenv('JIRA_URL'), username=os.getenv('JIRA_USERNAME'), password=os.getenv('JIRA_PASSWORD'),
                cloud=True)
    # for issue in unmatched_issues:
    #     print('h')
    issue_dict = {
        'project': {'key': 'DEVOPS'},
        'summary': summary,
        'description': description,
        'issuetype': {'name': 'Task'},
        'parent': {
            "key": epic_key
        }
    }
    new_issue = jira.issue_create(fields=issue_dict)
    print(f"Created story {new_issue['key']} with epic {epic_key} at {date_time()} IST")


def issues_in_epic(epic_key: str):
    """
    list available issues in a epic
    :param epic_key:
    :return:
    """
    # Initializing jira client
    load_dotenv()
    JIRA_URL = os.getenv('JIRA_URL')
    JIRA_USERNAME = os.getenv('JIRA_USERNAME')
    JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
    jira = Jira(url=os.getenv('JIRA_URL'), username=os.getenv('JIRA_USERNAME'), password=os.getenv('JIRA_PASSWORD'),
                cloud=True)

    url = f'{JIRA_URL}/rest/api/3/search'

    auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_PASSWORD)

    headers = {
        "Accept": "application/json"
    }

    query = {
        'jql': f'Parent = {epic_key}'
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )
    response_json = response.json()
    response_json_issues = response_json['issues']
    if not response_json_issues:
        issues_in_epic = []
    else:
        issues_in_epic = response_json['issues']

    epic_details = []
    for issues in issues_in_epic:
        issue = {}
        issue['key'] = issues['key']
        issue['issue_type'] = issues['fields']['issuetype']['name']
        issue['issue_summary'] = issues['fields']['summary']
        issue['description'] = 'NA'
        epic_details.append(issue)

    return epic_details


def compare_summaries_and_create_story(repo_names: list, organization: str, epic_key: str):
    """
    The function helps create stories by calling another function.
    :param issues_list:
    :param epic_details:
    :return:
    """
    epic_details = issues_in_epic(epic_key=epic_key)

    for repo in repo_names:
        # scan details
        issues_list = scan_for_dependabot_alerts_and_issues(organization=organization, repository=repo)
        if not issues_list:
            print(f'No dependabot security alerts found on {organization}/{repo} repository')
            continue
        create_story_true = compare_summaries_from_epic_and_scan(issues_list=issues_list, epic_details=epic_details)
        for issue in create_story_true:
            summary_from_gh = f"{issue['cve_id']} - {issue['repository']} - {issue['issue_severity']} - {issue['issue_summary']}"
            description_from_gh = issue['issue_description']
            summary_after_character_length_check = limit_string_length(input_string=summary_from_gh)
            description_after_character_length_check = limit_string_length(input_string=description_from_gh)

            create_story_under_epic(summary=summary_after_character_length_check,
                                    description=description_after_character_length_check, epic_key=epic_key)



def main():
    """testing script"""

    parser = argparse.ArgumentParser(description='Create Jira issues prograatically based on dependabot alerts')
    parser.add_argument("--epic_key", help="jira epic ID", type=str, required=True)
    parser.add_argument('--organization', help='Github org name', type=str, required=True)

    args = parser.parse_args()

    epic_key = args.epic_key
    organization = args.organization

    # List stories under an epic
    epic_details = issues_in_epic(epic_key=epic_key)

    # Repos in GitHub org
    repo_names = list_repos_in_org(org_name=organization)

    # compare summaries to decide to create a new story or not
    compare_summaries_and_create_story(repo_names=repo_names, organization=organization,
                                       epic_key=epic_key)



if __name__ == "__main__":
    main()
