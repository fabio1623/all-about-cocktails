import unittest
from Services.NexibleService import NexibleService

class TestNexibleService(unittest.TestCase):
    def setUp(self):
        self.nexible_service = NexibleService()
        
    def test_get_cocktails(self):
        cocktails = self.nexible_service.get_cocktails()
        self.assertTrue(len(cocktails) > 0)