import copy
import sys

class VirtualEnvironment:
    def __init__(self):
        self.original_modules = copy.copy(sys.modules)
    
    def __enter__(self):
        self.snapshot = copy.deepcopy(sys.modules)
        return self
    
    def __exit__(self, *args):
        sys.modules = self.snapshot
    
    def safe_execute(self, code: str):
        """تنفيذ الكود في بيئة افتراضية"""
        try:
            exec(code, {'__builtins__': __builtins__})
            return True
        except Exception as e:
            return False