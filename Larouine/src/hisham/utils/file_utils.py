import shutil
import hashlib
from pathlib import Path

class ExternalFileManager:
    def create_file_fingerprint(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def rollback_update(self, file_path: str, backup_hash: str):
        backup_file = f"{file_path}.backup_{backup_hash[:8]}"
        if Path(backup_file).exists():
            shutil.copy(backup_file, file_path)
            return True
        return False