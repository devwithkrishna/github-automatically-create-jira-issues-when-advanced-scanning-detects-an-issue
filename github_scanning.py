import os
from dotenv import load_dotenv
import requests

def scan_for_dependabot_alerts_and_issues(organization: str, repository: str):
    """
    scan github for github security scans and issues
    :return:
    """
    api_endpoint = f'https://api.github.com/repos/{organization}/{repository}/dependabot/alerts'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(url=api_endpoint, headers=headers)
    response_json = response.json()
    # print(response_json)
    issues_list = []
    for issue in response_json:
        dict = {}
        dict['dependancy'] = issue['dependency']['package']
        dict['issue_is_at'] = issue['dependency']['manifest_path']
        dict['cve_id'] = issue['security_advisory']['cve_id']
        dict['issue_summary'] = f'{issue["security_advisory"]["summary"]} - {repository}'
        dict['issue_description'] = issue['security_advisory']['description']
        dict['issue_severity'] = issue['security_advisory']['severity']
        dict['issue_created_at'] = issue['created_at']
        dict['repository'] = repository


        # add dict to list
        issues_list.append(dict)

    return issues_list

def main():
    """To test the scripts"""
    load_dotenv()
    organization = 'devwithkrishna'
    repository = 'programatically-create-delete-update-github-repository-secrets'

    issues_list = scan_for_dependabot_alerts_and_issues(organization=organization, repository=repository)


if __name__ == "__main__":
    main()