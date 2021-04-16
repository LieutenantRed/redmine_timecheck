#!/usr/bin/python3
from redminelib import Redmine
from typing import List
from html_eltex_loc import eltex_get_employee_status, Status
import yaml
import datetime


ymlconf = "config.yml"
config = yaml.safe_load(open(ymlconf))
defconfig = config['defconfig']
userconf = config['userconf']
timetracker = config['timetracker']
redmine = Redmine(
    defconfig['red'],
    key=userconf['key'],
    raise_attr_exception=('Project', 'Issue', 'WikiPage')
)


def get_current_tasks() -> List:
    tasks = []
    this_user = redmine.user.get('current')
    in_progress = filter(lambda task: task.status.id == 2, this_user.issues)
    for item in in_progress:
        tasks.append(item.id)
    return tasks


def commit_changes():
    try:
        summ = sum(timetracker['current_tasks'].values())
        for key, value in timetracker['current_tasks'].items():
            time_entry = redmine.time_entry.create(
                issue_id=key,
                spent_on=datetime.date.today(),
                hours=timetracker['online'] * value / summ,
                activity_id=9,  # Code
            )
            time_entry.save()
    except Exception:
        return


if __name__ == "__main__":
    # complete config info
    if config['userconf']['redname'] is None:
        this_user = redmine.user.get('current')
        userconf['redname'] = this_user.login
        with open(ymlconf, 'w') as file:
            yaml.dump(config, file)
    # commit existed changes if user goes offline
    if eltex_get_employee_status(userconf['redname']) != Status.work:
        # commit changes here
        commit_changes()
        # reset commited values
        timetracker['current_tasks'] = {}
        timetracker['online'] = None
        with open(ymlconf, 'w') as file:
            yaml.dump(config, file)
        exit()
    # find in_progress
    tasks = get_current_tasks()
    # update values in yaml file
    tracker = timetracker['current_tasks']
    for item in tasks:
        try:
            if tracker[item] is None:
                tracker[item] = 0
            else:
                tracker[item] = tracker[item] + 1
        except KeyError:  # value doesnt exist
            tracker[item] = 0
    if timetracker['online'] is None:
        timetracker['online'] = 0
    else:
        timetracker['online'] = timetracker['online'] + 1
    with open(ymlconf, 'w') as file:
            yaml.dump(config, file)
