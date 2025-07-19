import json
from pathlib import Path
from ..utils.file_utils import ExternalFileManager

class SmartFusionSystemPro:
    def __init__(self):
        self.config = self.load_config()
        self.file_manager = ExternalFileManager()
    
    def load_config(self):
        config_path = Path(__file__).parent.parent.parent / 'configs' / 'larouine.config.json'
        with open(config_path) as f:
            return json.load(f)
    
    def safe_self_update(self, new_code: str):
        current_file = Path(__file__).resolve()
        if self.file_manager.safe_edit_file(str(current_file), new_code):
            print("System core updated successfully!")
            return True
        return False