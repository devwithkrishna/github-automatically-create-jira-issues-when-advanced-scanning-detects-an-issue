import os
import json
import requests
from dotenv import load_dotenv
from atlassian import Jira

# Initializing jira client
load_dotenv()
JIRA_URL = os.getenv('JIRA_URL')
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')



# Function to create a story under a specific epic
def create_story_under_epic(epic_key, summary, description):
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
    # pic = new_issue.update(fields={'parent': {'id': epic_key}})

    return new_issue


def issues_in_epic(epic_key: str, board_id: int):
    """
    list available issues in a epic
    :param epic_key:
    :return:
    """
    jira = Jira(url=os.getenv('JIRA_URL'), username=os.getenv('JIRA_USERNAME'), password=os.getenv('JIRA_PASSWORD'),
                cloud=True)

    # todo

def get_board_id(project_key: str):
    # jira = Jira(url=os.getenv('JIRA_URL_0'), username=os.getenv('JIRA_USERNAME'), password=os.getenv('JIRA_PASSWORD'),
    #             cloud=True)
    response = requests.get(url=os.getenv('JIRA_URL_0'),auth=(os.getenv('JIRA_USERNAME'), os.getenv('JIRA_PASSWORD')))
    if response.status_code == 200:
        boards = response.json()['values']
        if boards:
            # Assuming you want the first board ID
            return boards[0]['id']
    return None

def main():
    """testing script"""
    # Replace these values with your specific details
    epic_key = 'DEVOPS-74'
    summary = 'New Story Summary135'
    description = 'Description -- of the new story'

    # Create the story
    # story = create_story_under_epic(epic_key, summary, description)
    # print(f"Created story {story['key']} under epic {epic_key}")

    # List stories under an epic
    stories = issues_in_epic(epic_key=epic_key, board_id=1)

    # get_board_id('DEVOPS')

if __name__ == "__main__":
    main()
