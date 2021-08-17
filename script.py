#!/usr/bin/env python

import json

import asana


AUTH_FILE = 'auth.json'


with open(AUTH_FILE) as f:
    j = json.load(f)
    asana_key =  j['key']
    workspace_gid = j['workspace']

client = asana.Client.access_token(asana_key)
# me = client.users.me()
# print(me)

# opts = {'tags.any':'active'}
# result = client.tasks.search_tasks_for_workspace(workspace_gid, opts, opt_pretty=True)

# opts = {'workspace':workspace_gid,}
# result = client.tasks.get_tasks(opts, opt_pretty=True)

task_list = client.user_task_lists.get_user_task_list_for_user('me', {'workspace':workspace_gid})

res = client.user_task_lists.get_user_task_list(task_list['gid'])

opts = {'completed_since':'now'}
fields = ['this.name',
          'this.due_on',
          'this.memberships.project.name',
          'this.memberships.section.name',
          'this.tags.name']
res = client.tasks.find_by_user_task_list(res['gid'], opts, opt_fields=fields)

def has_tag(r, tag):
    for t in r['tags']:
        if tag == t['name']:
            return True
    return False



{'gid': '1200716274440367',
 'memberships': [
     {'project': {'gid': '1200601501511683', 'name': 'Electronics 340 2021'},
      'section': {'gid': '1200716274440346', 'name': 'Tasks'}}
    ],
 'name': 'Setup syllabus',
 'tags': [{'gid': '682001759886391', 'name': 'active'}]}


active_tasks = []
for r in res:
    if has_tag(r, 'active'):
        active_tasks.append(r)

for task in active_tasks:
    for m in task['memberships']:
        t_name = task['name']
        due = task['due_on'] or ''
        p_name = m['project']['name']
        s_name = m['section']['name']
        if s_name == 'Untitled section':
            s_name = 'none'

        print(f'{p_name:20.20s} : {s_name:10.10s} : {t_name} {due}')

