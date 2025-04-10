import json
from collections import defaultdict

class AIAdvisor:
    def __init__(self):
        self.knowledge_base = self._load_knowledge()
    
    def suggest_merge_strategy(self, new_code: str) -> dict:
        """
        اقتراح استراتيجية دمج بناء على الخبرة السابقة
        """
        features = self._analyze_code_features(new_code)
        return {
            'strategy': self._select_strategy(features),
            'confidence': 0.85
        }
    
    def _analyze_code_features(self, code: str) -> dict:
        # تحليل خصائص الكود
        return {
            'complexity': self._calculate_complexity(code),
            'dependencies': len(self._find_dependencies(code))
        }
    
    def _load_knowledge(self):
        try:
            with open('knowledge_base.json') as f:
                return json.load(f)
        except:
            return defaultdict(int)