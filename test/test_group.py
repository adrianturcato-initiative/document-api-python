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

    def setUp(self):
        self.wb = Workbook(TEST_TWB_FILE)
        # Assume the first dashboard in the file
        self.datasources = self.wb.datasources
        self.user_filter = self.wb.user_filter
        self.access_permissions = self.wb.access_permissions

    def test_groups_in_datasource(self):
        self.assertEqual(len(self.datasources[0].groups), 0)
        self.assertEqual(len(self.datasources[1].groups), 0)
        self.assertEqual(len(self.datasources[2].groups), 0)
        self.assertEqual(len(self.datasources[3].groups), 1)
        self.assertEqual(len(self.datasources[4].groups), 4)

    def test_user_filter_group_in_datasource(self):
        self.assertTrue(self.wb.user_filter)

    def test_user_filter_access_permissions_table(self):
        self.assertEqual(len(self.access_permissions.group_permissions), 4)
        self.assertEqual(self.access_permissions.group_permissions[0].name, "Jazz Pharmaceuticals-USA-All-Editor")
        self.assertEqual(self.access_permissions.group_permissions[0].advertisers[0], "Jazz Pharma - ADKT Unbranded DTC")

