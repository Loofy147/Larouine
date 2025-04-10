import json
import logging
import os
import requests
import yaml
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Optional

# إعداد السجل لتوثيق العمليات
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# الإعدادات الافتراضية
DEFAULT_CONFIG = {
    "github_settings": {
        "repo_branch": "main"
    },
    "target_components": []
}


# تعريف النماذج باستخدام Pydantic
class ComponentConfig(BaseModel):
    name: str
    keywords: List[str]
    required: bool
    min_stars: int
    max_age_days: Optional[int] = 730


class GitHubConfig(BaseModel):
    api_token: str = os.getenv("GITHUB_API_TOKEN", "")
    repo_owner: str
    repo_name: str
    repo_branch: str


class ProjectConfig(BaseModel):
    project_name: str
    target_components: List[ComponentConfig]
    github_settings: GitHubConfig


# الوظائف الرئيسية


def load_config(file_path: str) -> ProjectConfig:
    """تحميل التكوين من ملف JSON"""
    if not os.path.exists(file_path):
        logging.error(f"Configuration file not found: {file_path}")
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    with open(file_path, 'r') as f:
        raw_config = json.load(f)

    # دمج الإعدادات الافتراضية
    merged_config = {**DEFAULT_CONFIG, **raw_config}

    try:
        return ProjectConfig(**merged_config)
    except ValidationError as e:
        logging.error(f"Invalid configuration: {e}")
        raise ValueError(f"Invalid configuration: {e}")


def save_config(config: ProjectConfig, file_path: str):
    """حفظ التكوين إلى ملف JSON"""
    with open(file_path, 'w') as f:
        json.dump(config.dict(), f, indent=4)
    logging.info(f"Configuration saved to {file_path}")


def load_config_from_url(url: str) -> ProjectConfig:
    """تحميل التكوين من URL"""
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to fetch configuration from URL: {url}")
        raise ValueError(f"Failed to fetch configuration from URL: {url}")

    raw_config = response.json()
    try:
        return ProjectConfig(**raw_config)
    except ValidationError as e:
        logging.error(f"Invalid configuration: {e}")
        raise ValueError(f"Invalid configuration: {e}")


def export_config_to_yaml(config: ProjectConfig, file_path: str):
    """تصدير التكوين إلى ملف YAML"""
    with open(file_path, 'w') as f:
        yaml.dump(config.dict(), f)
    logging.info(f"Configuration exported to {file_path}")


def validate_config(file_path: str):
    """التحقق من صحة ملف التكوين"""
    try:
        load_config(file_path)
        logging.info(f"The configuration file {file_path} is valid.")
    except Exception as e:
        logging.error(f"The configuration file {file_path} is invalid: {e}")
        raise e


def update_config(file_path: str, updates: Dict):
    """تحديث قيم التكوين"""
    config = load_config(file_path)
    for key, value in updates.items():
        if hasattr(config, key):
            setattr(config, key, value)
    save_config(config, file_path)


def compare_configs(config1: ProjectConfig, config2: ProjectConfig) -> Dict:
    """مقارنة ملفي تكوين"""
    differences = {}
    for field in config1.__fields__.keys():
        value1 = getattr(config1, field, None)
        value2 = getattr(config2, field, None)
        if value1 != value2:
            differences[field] = {"old": value1, "new": value2}
    return differences