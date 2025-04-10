import subprocess
from typing import Dict

def push_to_github(repo_path: str, commit_message: str):
    try:
        subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
        subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "-C", repo_path, "push", "origin", "main"], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git operation failed: {e}")

def setup_repository(config: Dict):
    repo_url = f"git@github.com:{config['repo_owner']}/{config['repo_name']}.git"
    try:
        subprocess.run(["git", "clone", repo_url], check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to clone repository")
