import unittest
import json
import os
from pathlib import Path

from equit_ease.parser.parse import UserConfigParser

class TestUserConfigParser(unittest.TestCase):
    """Testing methods from the UserConfigParser class."""
    user_home_dir = str(Path.home()) 
    equit_ease_dir = os.path.join(user_home_dir, ".equit_ease")
    lists_file_path = Path(os.path.join(equit_ease_dir, "lists"))

    def setUp(self):
        self.list_name = "Test"
        self.list_file_contents = open(self.lists_file_path, "r").read().splitlines()
        self.parser = UserConfigParser(self.list_name, self.list_file_contents)
        self.equities, _ = self.parser.format_equity_lists()

    def tearDown(self):
        self.equity = None
        self.list_file_contents = None
        self.parser = UserConfigParser
        self.equities = None
    


