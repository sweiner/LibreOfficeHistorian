"""
Libre Office Historian

Author: Scott Weiner
Description: This application can provide a change synopsis of a particular function in the Libre Office
                source code repository
Date: 11/5/2023
"""

import argparse
import subprocess
import config
import os
import openai
from models import GitLogData, GerritChangeData, BugzillaBugData


def find_file(root_dir, target_filename):
    for root, dirs, files in os.walk(root_dir):
        if target_filename in files:
            return os.path.join(root, target_filename)

    # If the file is not found
    return None


if __name__ == '__main__':
    # Create an ArgumentParser
    parser = argparse.ArgumentParser()

    # Define a required argument
    parser.add_argument('file', help='The file which contains the function')
    parser.add_argument('function', help='The function which we want the history of')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the value of the required argument
    source_file_path = args.file
    source_function = args.function

    # Find the file
    source_file = find_file(config.REPOSITORY_PATH, source_file_path)
    if not source_file:
        raise FileNotFoundError

    # Get the GIT info
    command = [f"{config.GIT_PATH}",
               f"--git-dir={config.REPOSITORY_PATH}/.git",
               "log",
               f"-L:{source_function}:{source_file}"]

    output = subprocess.check_output(command, cwd=config.REPOSITORY_PATH, universal_newlines=True)

    # Populate the GitLogData model and extract the change IDs for this function
    gd = GitLogData(output)
    change_ids = gd.get_change_ids()

    # For each change, check if there is a bug report, if there is, populate a bug report model and save it off
    bugzilla_id = ""
    history = list()

    for change in change_ids:
        gcd = GerritChangeData(change)
        bugzilla_id = gcd.extract_bugzilla_id()
        if bugzilla_id:
            bbd = BugzillaBugData(bugzilla_id)
            history.append(bbd.extract_comments())

    # I have to scale down the tokens due to max limits on gpt-3.5, full input was over 5000
    openai.api_key = config.OPEN_AI_KEY
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system",
                   "content": "You are an expert software engineer who is skilled at providing detailed histories about the software from bug reports."},
                  {"role": "user",
                   "content": f"Given the following list of bug reports, times and comments, please provide a synopsis of the history in chronological order.  {history.pop()[0:5]}"}]
    )

    print(completion.choices[0].message)
