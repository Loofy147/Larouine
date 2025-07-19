import shutil
from pathlib import Path

class ExternalFileManager:
    def safe_edit(self, file_path: str, new_content: str):
        backup_path = f"{file_path}.bak"
        shutil.copyfile(file_path, backup_path)
        try:
            with open(file_path, 'w') as f:
                f.write(new_content)
            return True
        except:
            shutil.copyfile(backup_path, file_path)
            return False