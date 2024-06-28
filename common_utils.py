def limit_string_length(input_string: str, max_length=254):
    """
    This function is created to trim the long summary and descriptions of github vumnerability.
    Jira is having 255 character limits for summaries. so doing for both
    :param input_string:
    :param max_length:
    :return:
    """
    # Check the length of the string
    string_length = len(input_string)
    print(f"Original string length: {string_length}")

    # Limit the string to max_length characters
    if string_length > max_length:
        input_string = input_string[:max_length]
        print(f"String was truncated to {max_length} characters.")

    return input_string


def compare_summaries_from_epic_and_scan(epic_details: list[dict], issues_list:list[dict]):
    """
    this function is to compare the stories existing in epic with the github dependabot alerts
    available to not create duplicate stories. this works to ensure that duplicate wont happen
    -POC-
    :param epic_details:
    :param issues_list:
    :return:
    """
    create_story_true = []
    print(epic_details)
    print(issues_list)
    for issue in issues_list:
        summary_from_gh = f"{issue['cve_id']} - {issue['repository']} - {issue['issue_severity']}"
        summary_from_gh_split = summary_from_gh.split(' - ')
        found_matching_story = False
        for story in epic_details:
            story_summary = story['issue_summary']
            story_summary_split = story_summary.split(' - ')
            if summary_from_gh_split[:3] == story_summary_split[:3]:
                print(f'Story already created for this. Story key {story["key"]}')
                found_matching_story = True
                break
        if not found_matching_story:
            create_story_true.append(issue)
        # create_story_true.append(issue)
    return create_story_true



def main():
    """ To test the code"""
    original_string = "This is a very long string..."  # Replace with your actual string
    limited_string = limit_string_length(original_string)

if __name__ == "__main__":
    main()