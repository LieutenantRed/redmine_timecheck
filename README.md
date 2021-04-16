# redmine_timechecker

Collect information about user activity from Redmine to yaml file, commit labor costs to the server.

### Usage

Set up yours checker enviroment by editing [config.yml](https://gitlab.eltex.loc/irina.emelyanova/redmine_timechecker/blob/master/README.md).
```sh
userconf:
  key: <%your access key%>
  name: null
  redname: null
```

Then install requirements and start the [main.py](https://gitlab.eltex.loc/irina.emelyanova/redmine_timechecker/blob/master/main.py)
```sh
pip3 install -r requirements.txt
chmod +x main.py cronjob.py
./main.py
```

To watch created cron task do
```sh
crontab -e
```