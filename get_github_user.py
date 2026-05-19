#!/usr/bin/env python3
"""Get GitHub user info from token"""

import requests

GITHUB_TOKEN = "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"

url = "https://api.github.com/user"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    user_data = response.json()
    print("✅ GitHub user info:")
    print(f"  Username: {user_data['login']}")
    print(f"  Name: {user_data.get('name')}")
    print(f"  Email: {user_data.get('email')}")
    print(f"  Repos URL: {user_data['repos_url']}")
else:
    print(f"❌ Failed to get user info: {response.status_code}")
    print(response.text)
