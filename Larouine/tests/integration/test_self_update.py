import unittest
from src.hisham.core.fusion_core import SmartFusionSystemPro

class TestSelfUpdate(unittest.TestCase):
    def setUp(self):
        self.system = SmartFusionSystemPro()
    
    def test_safe_update(self):
        dummy_code = "print('New improved system!')"
        result = self.system.safe_self_update(dummy_code)
        self.assertTrue(result)
    
    def tearDown(self):
        # استعادة النسخة الأصلية بعد الاختبار
        pass

import unittest
from src.hisham.core.fusion_core import FusionCore

class TestSelfUpdate(unittest.TestCase):
    def test_self_healing(self):
        core = FusionCore()
        # اختبار قدرة النظام على استعادة نفسه هنا
        self.assertTrue(core.self_heal())


import unittest
import time
from pathlib import Path
from src.hisham.core.evolution_loop import EvolutionLoop

class TestSelfUpdate(unittest.TestCase):
    def test_auto_update(self):
        # إنشاء ملف تحديث تجريبي
        test_update = Path(__file__).parent.parent.parent / 'loop_brain' / 'pending' / 'test_update.py'
        test_update.write_text("# Test Update Content")
        
        # بدء الحلقة التطورية
        loop = EvolutionLoop()
        loop.interval = 1  # 1 ثانية للاختبار
        loop.start()
        
        time.sleep(2)  # انتظار دورة واحدة
        
        # التحقق من التطبيق
        current_code = Path(__file__).read_text()
        self.assertIn("Test Update Content", current_code)
        
        # تنظيف
        test_update.unlink()