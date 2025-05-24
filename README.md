# redmine-reminder-slack

## Usage

```
export REDMINE_URL=http://example.com
export REDMINE_API_KEY=xxx
export REDMINE_PROJECT=yyy
export SLACK_WEBHOOK_URL=zzz

python3 notify_redmine.py
```

## Scheduling

every day 9:00 AM

```
sudo systemd-run --on-calendar='*-*-* 00:09:00' --timer-property=AccuracySec=1s /bin/bash /path/to/slack-notify/run.sh
```
