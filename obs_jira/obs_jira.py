# Copyright 2023 Daniel Mellado.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from jira import JIRA
from prettytable import PrettyTable

import logging
import os

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

jira = JIRA(server='https://issues.redhat.com/',
            token_auth=os.environ['JIRA_API_TOKEN'])


def get_issues_by_project(project='MON'):
    return jira.search_issues('project=' + project)


def get_current_sprint_issues(project='MON'):
    jql_query = 'project=' + project + ' AND sprint in openSprints()'
    return jira.search_issues(jql_query)


def get_current_user_issues():
    jql_query = 'assignee=currentuser() AND sprint in openSprints()'
    return jira.search_issues(jql_query)


def print_issues(project='MON', currentuser=False):
    issues = get_current_sprint_issues(project=project)
    if currentuser:
        issues = get_current_user_issues()
    x = PrettyTable()
    x.field_names = ["Summary", "Assignee", "Reporter", "Status"]
    x.align["Summary"] = "l"
    for i in issues:
        x.add_row([str(i.key) + " " + str(i.fields.summary),
                   str(i.fields.assignee),
                   str(i.fields.reporter),
                   str(i.fields.status)])
    print(x.get_string(sortby="Assignee"))


def create_issue(summary, description="", issue_type='Bug', project='MON',
                 assign=False):
    issue_dict = {
        'project': {'key': project},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issue_type}
    }

    if project == 'OCPBUGS':
        issue_dict['versions'] = [{'name': '4.14'}]
        # severity
        issue_dict['customfield_12316142'] = {'value': 'Low'}
        # target_version
        issue_dict['components'] = [{'name': 'Monitoring'}]
        issue_dict['customfield_12319940'] = [{'name': '4.14.0'}]
        issue_dict['priority'] = {'name': 'Normal'}

    issue = jira.create_issue(fields=issue_dict)
    LOG.info("Created new Issue: %s", issue.key)
    sprint_id = jira.sprint(id=jira._get_sprint_field_id())
    jira.add_issues_to_sprint(sprint_id, [issue.id])
    LOG.info("Added Issue %s to current sprint", issue.key)

    if assign:
        assignee = jira.myself().get('name')
        issue.update(assignee={'name': str(assignee)})
        LOG.info("Setting assignee to: %s", assignee)


def delete_issue(issue_id):
    issue = jira.issue(issue_id)
    LOG.info("Deleting Issue: %s", issue_id)
    issue.delete()

# create_issue(summary='Skip false positives
# for golangci-lint unused violations',
#              project='OCPBUGS', assign=True)
