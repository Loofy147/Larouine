import ast

class DependencyTracker:
    def analyze(self, code: str):
        tree = ast.parse(code)
        dependencies = {
            'imports': [],
            'functions': [],
            'classes': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dependencies['imports'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                dependencies['imports'].append(f"{module}.{node.names[0].name}")
        
        return dependencies