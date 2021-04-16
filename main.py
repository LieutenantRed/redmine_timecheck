#!/usr/bin/python3

from crontab import CronTab
from os import getcwd as pwd

# use crontab -e to edit commands in eour's user cronfile if needed
# use crontab -l to show all cronjobs

with CronTab(user=True) as cron:
	location = pwd()
	job = cron.new(command=f'{location}/cronjop.py')
	job.hour.every(1)
	job.set_comment("Timechecker for redmine")
	cron.write()