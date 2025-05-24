import os
import requests
from datetime import datetime, timedelta

REDMINE_URL = os.environ['REDMINE_URL']
REDMINE_API_KEY = os.environ['REDMINE_API_KEY']
REDMINE_PROJECT = os.environ['REDMINE_PROJECT']
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

def get_issues_due_within(days=3):
    today = datetime.utcnow().date()
    due_date = today + timedelta(days=days)

    url = f"{REDMINE_URL}/issues.json"
    params = {
        'project_id': REDMINE_PROJECT,
        'key': REDMINE_API_KEY,
        'status_id': 'open',
        'due_date': f"<={due_date.isoformat()}",
        'limit': 100,
        'include': 'assigned_to'
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('issues', [])

def send_to_slack(issues):
    if not issues:
        message = "締め切り3日以内のチケットはありません。"
    else:
        message = "*締め切り3日以内のチケット一覧:*\n"
        for issue in sorted(issues, key=lambda x: x.get("due_date", "")):
            issue_id = issue["id"]
            subject = issue["subject"]
            due_date = issue.get("due_date", "未設定")
            assigned_to = issue.get("assigned_to", {}).get("name", "未割り当て")
            issue_url = f"{REDMINE_URL}/issues/{issue_id}"

            message += f"- <{issue_url}|{due_date}>: ({assigned_to}) {subject}\n"

    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    issues = get_issues_due_within(3)
    send_to_slack(issues)
