import os.path
import unittest

from tableaudocumentapi import Workbook

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)

TEST_TWB_FILE = os.path.join(
    TEST_ASSET_DIR,
    'group_test.twb'
)

class GroupTWB(unittest.TestCase):

    def test_groups_in_datasource(self):
        self.wb = Workbook(TEST_TWB_FILE)
        self.datasources = self.wb.datasources
        self.assertEqual(len(self.datasources[0].groups), 0)
        self.assertEqual(len(self.datasources[1].groups), 0)
        self.assertEqual(len(self.datasources[2].groups), 0)
        self.assertEqual(len(self.datasources[3].groups), 1)
        self.assertEqual(len(self.datasources[4].groups), 4)

class UserFilterGroupTWB(unittest.TestCase):

    def test_user_filter_group_in_datasource(self):
        self.wb = Workbook(TEST_TWB_FILE)
        self.user_filter = self.wb.user_filter
        self.assertTrue(self.wb.user_filter)
