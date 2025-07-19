import ast

class CodeAnalyzer:
    def analyze_structure(self, code: str):
        tree = ast.parse(code)
        return {
            'functions': [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)],
            'classes': [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        }