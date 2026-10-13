#!/usr/bin/env python3
"""Script to create GitHub private repo and push code"""

import os
import sys
import requests
import subprocess

# Configuration
GITHUB_TOKEN = "REDACTED_GITHUB_TOKEN"
REPO_NAME = "agent_perpetual_evolution_system"
REPO_DESCRIPTION = "Agent Perpetual Evolution System - Advanced AI system with quantum and AGI capabilities"
GITHUB_USER = "17683995446"


def create_github_repo():
    """Create private GitHub repo"""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": REPO_NAME,
        "description": REPO_DESCRIPTION,
        "private": True,
        "auto_init": False
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code in (201, 422):
        if response.status_code == 201:
            print("✅ GitHub private repository created successfully!")
        else:
            print("⚠️ Repository may already exist, continuing...")
        return True
    else:
        print(f"❌ Failed to create repo: {response.status_code}")
        print(response.text)
        return False


def push_code():
    """Push code to GitHub"""
    # Add remote origin if not exists
    try:
        # Check if remote exists
        remotes = subprocess.check_output(
            ["git", "remote", "-v"], 
            universal_newlines=True, 
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        if "origin" in remotes:
            # Remove existing origin
            subprocess.run(
                ["git", "remote", "remove", "origin"],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                check=True
            )
    except Exception as e:
        print(f"ℹ️ No existing origin found, adding new: {e}")
    
    # Add origin
    repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
    try:
        subprocess.run(
            ["git", "remote", "add", "origin", repo_url],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            check=True
        )
        
        # Push
        subprocess.run(
            ["git", "push", "-u", "origin", "master"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            check=True
        )
        print("✅ Code pushed to GitHub successfully!")
        print(f"📦 Repository URL: https://github.com/{GITHUB_USER}/{REPO_NAME}")
        return True
    except Exception as e:
        print(f"❌ Error pushing code: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting GitHub repository setup...")
    
    # Create repo
    if create_github_repo():
        # Push code
        push_code()
    
    print("✅ Done!")
