import json
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Optional


class ComponentConfig(BaseModel):
    name: str
    keywords: List[str]
    required: bool
    min_stars: int
    max_age_days: Optional[int] = 730


class GitHubConfig(BaseModel):
    api_token: str
    repo_owner: str
    repo_name: str
    repo_branch: str


class ProjectConfig(BaseModel):
    project_name: str
    target_components: List[ComponentConfig]
    github_settings: GitHubConfig


def load_config(file_path: str) -> ProjectConfig:
    with open(file_path, "r") as f:
        raw_config = json.load(f)

    try:
        return ProjectConfig(**raw_config)
    except ValidationError as e:
        raise ValueError(f"Invalid configuration: {e}")
