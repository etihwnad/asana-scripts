#!/usr/bin/env python

import json
from datetime import datetime as dt

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



# {'gid': '1200716274440367',
#  'memberships': [
#      {'project': {'gid': '1200601501511683', 'name': 'Electronics 340 2021'},
#       'section': {'gid': '1200716274440346', 'name': 'Tasks'}}
#     ],
#  'name': 'Setup syllabus',
#  'tags': [{'gid': '682001759886391', 'name': 'active'}]}


active_tasks = []
for r in res:
    if has_tag(r, 'active'):
        active_tasks.append(r)

today = dt.now()
tasks = []
for task in active_tasks:
    for m in task['memberships']:
        t = {}
        t['name'] = task['name']
        due_str = task['due_on']
        t['due_on'] = due_str
        if due_str:
            due_date = dt.strptime(due_str, '%Y-%m-%d')
            days_due = (due_date - today).days + 1
            t['days_due'] = days_due

        t['p_name'] = m['project']['name']

        s_name = m['section']['name']
        if s_name == 'Untitled section':
            s_name = 'none'
        t['s_name'] = m['section']['name']
        tasks.append(t)


for t in sorted(tasks, key=lambda x: x['days_due']):
    p_name = t['p_name']
    s_name = t['s_name']
    t_name = t['name']
    days_due = t['days_due']

    if days_due == 0:
        due = '***'
    else:
        due = f'{days_due:+2d}'

    # print(f'{p_name:16.16s} : {s_name:10.10s} : {t_name} {due}')
    print(f'{p_name:24.24s} - {t_name} {due}')

