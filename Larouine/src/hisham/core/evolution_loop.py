import time
from pathlib import Path

class EvolutionLoop:
    def __init__(self):
        self.loop_active = True
        self.interval = 300  # 5 دقائق
        
    def start(self):
        while self.loop_active:
            self.check_pending_updates()
            time.sleep(self.interval)
            
    def check_pending_updates(self):
        pending_dir = Path(__file__).parent.parent.parent / 'loop_brain' / 'pending'
        for file in pending_dir.glob('*.py'):
            print(f"Processing update: {file.name}")
            # هنا سيتم إضافة منطق الدمج لاحقًا

import time
import threading
from pathlib import Path
from ..modules.smart_fusion_system import SmartFusionSystem

class EvolutionLoop:
    def __init__(self):
        self.is_active = True
        self.fusion = SmartFusionSystem()
        self.interval = 60  # 60 ثانية
        
    def start(self):
        """بدء الحلقة التطورية في خيط منفصل"""
        thread = threading.Thread(target=self.run)
        thread.start()
        
    def run(self):
        while self.is_active:
            self.check_pending_updates()
            time.sleep(self.interval)
            
    def check_pending_updates(self):
        pending_dir = Path(__file__).parent.parent.parent / 'loop_brain' / 'pending'
        for update_file in pending_dir.glob('*.py'):
            self.process_update(update_file)
            
    def process_update(self, file_path):
        with open(file_path, 'r') as f:
            new_code = f.read()
        
        current_code = self.get_current_code()
        merged = self.fusion.merge_code(current_code, new_code)
        self.apply_update(merged)
        
    def get_current_code(self):
        current_file = Path(__file__)
        with open(current_file, 'r') as f:
            return f.read()
            
    def apply_update(self, new_code):
        current_file = Path(__file__)
        with open(current_file, 'w') as f:
            f.write(new_code)