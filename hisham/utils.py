import subprocess
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)

def push_to_github(repo_path: str, commit_message: str, branch: str = "main"):
    try:
        logging.info(f"Pushing changes to branch {branch} in repository at {repo_path}")
        subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
        subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "-C", repo_path, "push", "origin", branch], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Git operation failed: {e}")
        raise RuntimeError(f"Git operation failed: {e}")

from .config_manager import GitHubConfig

def setup_repository(config: GitHubConfig, protocol: str = "ssh"):
    if protocol not in ["ssh", "https"]:
        raise ValueError("Invalid protocol specified. Use 'ssh' or 'https'.")
    
    if protocol == "ssh":
        repo_url = f"git@github.com:{config.repo_owner}/{config.repo_name}.git"
    else:
        repo_url = f"https://github.com/{config.repo_owner}/{config.repo_name}.git"
    
    try:
        logging.info(f"Cloning repository from {repo_url}")
        subprocess.run(["git", "clone", repo_url], check=True)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to clone repository")
        raise RuntimeError("Failed to clone repository") from e