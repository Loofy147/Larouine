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