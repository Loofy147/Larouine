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