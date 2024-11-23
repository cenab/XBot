# tests/test_xbot.py

import unittest
from bots.xbot import XBot

class TestXBot(unittest.TestCase):
    def setUp(self):
        self.bot = XBot(config_path='config/xbot_character.json', table_name='test_xbot_data')

    def test_ingest_data(self):
        try:
            self.bot.ingest_data()
            # Further assertions can be added based on database content
            self.assertTrue(True)  # Placeholder
        except Exception as e:
            self.fail(f"Ingest data failed with exception: {e}")

    def test_process_query(self):
        try:
            response = self.bot.process_query("What is Machine Learning?")
            self.assertIsInstance(response, str)
            self.assertTrue(len(response) > 0)
        except Exception as e:
            self.fail(f"Process query failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
