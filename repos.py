import os
import requests
import argparse
from dotenv import load_dotenv

def list_repos_in_org(org_name: str):
    """
    list all repos in github organization using rest api repo end point
    :param org_name:
    :return:
    """
    repo_endpoint = f'https://api.github.com/orgs/{org_name}/repos'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GH_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {
        'sort': 'created',
        'per_page': 30,
        'page': 1
    }

    # List to hold all repositories
    all_repositories = []
    # Paginate through all pages
    while True:
        # Make the GET request with query parameters
        response = requests.get(url=repo_endpoint, headers=headers, params=params)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON response
            repositories = response.json()
            if not repositories:
                break
            all_repositories.extend(repositories)
            params["page"] += 1
        else:
            print(f"Failed to fetch repositories: {response.status_code}")
            break

    # response = requests.get(url=repo_endpoint, headers=headers)
    # response_json = response.json()
    repo_names = []
    for repos in all_repositories:
        repo_names.append(repos['name'])

    return repo_names


def main():
    """ To test the script"""
    load_dotenv()
    parser = argparse.ArgumentParser(description='List github organization repos')
    parser.add_argument('--organization', help='Github org name', type=str, required=True)
    args = parser.parse_args()
    organization = args.organization
    repo_names = list_repos_in_org(org_name=organization)


if __name__ == "__main__":
    main()