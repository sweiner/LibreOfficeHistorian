import re
import config
import requests
import json


class GitChangeData:
    commit_id = ""
    author = ""
    date = ""
    message = ""
    diff = ""
    change_id = ""

    commit_pattern = r'commit\s[0-9a-f]+\n'
    author_pattern = r'Author: [A-Za-z\s]+ <[A-Za-z@.]+>'
    date_pattern = r'Date:\s+(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} \d{2}:\d{2}:\d{2} \d{4} [+-]\d{4}'
    message_pattern = r'(?<=[+-]\d{4})[\s\S]*?(?=\ndiff --git)'
    change_id_pattern = r'Change-Id: (\w{40})'

    def __init__(self, raw_change):
        # The handlers are there to handle blank data in the git log

        try:
            self.commit_id = re.search(self.commit_pattern, raw_change).group(0).strip().split(" ")[1]
        except AttributeError:
            pass

        try:
            self.author = re.search(self.author_pattern, raw_change).group(0).strip().split(":")[1].strip()
        except AttributeError:
            pass

        try:
            self.date = re.search(self.date_pattern, raw_change).group(0).strip().split(":")[1].strip()
        except AttributeError:
            pass

        try:
            self.message = re.search(self.message_pattern, raw_change).group(0).strip()
        except AttributeError:
            pass
        try:
            self.change_id = re.search(self.change_id_pattern, raw_change).group(0).strip().split(":")[1].strip()
        except AttributeError:
            pass

    def __str__(self):
        return f"{self.commit_id}\n{self.author}\n{self.date}\n{self.message}\n{self.change_id}\n"


class GitLogData:
    changes = list()

    def parse_commit_data(self, data):
        # Define the regular expression pattern to match commit lines
        commit_pattern = r'commit\s[0-9a-f]+\n'

        # Split the data into tokens using the commit pattern as the delimiter
        tokens = re.split(commit_pattern, data)[1:]  # [1:] to skip the empty string at the beginning

        # Remove leading and trailing whitespace from each token
        tokens = [token.strip() for token in tokens]

        # Add the commit id to the beginning of each token
        tokens = [f'{commit_id}\n{token}' for commit_id, token in
                  zip(re.findall(commit_pattern, data), tokens)]

        return tokens

    def __init__(self, raw_output):
        data = self.parse_commit_data(raw_output)
        for d in data:
            cd = GitChangeData(d)
            self.changes.append(cd)

    def get_change_ids(self):
        change_id_list = list()
        for c in self.changes:
            if c.change_id:
                change_id_list.append(c.change_id)

        return change_id_list


class GerritChangeData:
    change_id = ""
    response_data = dict()
    bugzilla_id = ""

    def request_change(self):
        url = config.GERRIT_URL + '/changes/' + str(self.change_id)
        response = requests.get(url)

        if response.status_code == 200:
            self.response_data = response.text
            # Clean this response data.  There is some oddness in the API response and extra characters are generated
            # For some reaosn
            split = self.response_data.split("\n")
            if len(split) > 1:
                self.response_data = split[1]
            else:
                self.response_data = split[0]

            try:
                self.response_data = json.loads(self.response_data)
            except json.JSONDecodeError:
                print("Could not decode Gerrit change data response")
        else:
            # print(f"Request failed with status code: {response.status_code}")
            self.response_data = None

    def extract_bugzilla_id(self):
        bugzilla_pattern = r'([0-9A-Za-z]+#)([0-9]+)'
        self.request_change()

        if self.response_data:
            match = re.search(bugzilla_pattern, self.response_data['subject'])
            if match:
                self.bugzilla_id = match.group(2)

        return self.bugzilla_id

    def __init__(self, change_id):
        self.change_id = change_id


class BugzillaBugData:
    bug_id = ""
    comments = list()
    response_data = ""

    def __init__(self, bug_id):
        self.bug_id = bug_id
        self.request_bug()

        if self.response_data:
            self.comments = self.response_data['bugs'][f'{self.bug_id}']['comments']

    def request_bug(self):
        url = config.BUGZILLA_URL + f"/rest/bug/{self.bug_id}/comment"
        response = requests.get(url)

        if response.status_code == 200:
            self.response_data = response.json()
        else:
            pass
            # print(f"Request failed with status code: {response.status_code}")

    def extract_comments(self):
        comment_list = list()
        for comment in self.comments:
            comment_list.append([comment['time'], comment['text']])

        return comment_list


