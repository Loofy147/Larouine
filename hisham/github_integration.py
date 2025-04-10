import requests
from typing import Dict, List
from datetime import datetime
from .config_manager import ComponentConfig

class GitHubAPI:
    def __init__(self, api_token: str):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {api_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def search_repositories(self, component: ComponentConfig) -> List[Dict]:
        # بناء الاستعلام باستخدام كلمات المفتاح
        query = " ".join(component.keywords)
        url = f"{self.base_url}/search/repositories?q={query}"

        params = {
            "sort": "stars",
            "order": "desc",
            "per_page": 20
        }

        if component.min_stars:
            params["q"] += f" stars:>={component.min_stars}"

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return self._filter_results(response.json()["items"], component)

    def _filter_results(self, items: List[Dict], component: ComponentConfig) -> List[Dict]:
        filtered = []
        for repo in items:
            last_updated = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
            age_days = (datetime.now() - last_updated).days

            if age_days > component.max_age_days:
                continue

            filtered.append({
                "name": repo["name"],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "last_updated": repo["updated_at"],
                "license": repo["license"]["key"] if repo["license"] else None,
                "score": self._calculate_score(repo, component)
            })

        return sorted(filtered, key=lambda x: x["score"], reverse=True)

    def _calculate_score(self, repo: Dict, component: ComponentConfig) -> float:
        score = 0.0

        # حساب العامل المتعلق بالتحديث
        last_updated = datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        days_since_update = (datetime.now() - last_updated).days
        recency_score = max(0, 1 - (days_since_update / 365))

        # حساب عامل الشهرة
        popularity_score = min(repo["stargazers_count"] / 1000, 1)

        # حساب النتيجة النهائية
        score = (recency_score * 0.6) + (popularity_score * 0.4)
        return round(score * 100, 2)
