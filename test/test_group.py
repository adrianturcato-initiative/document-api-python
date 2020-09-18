import os.path
import unittest
import hashlib

from tableaudocumentapi import Workbook

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)

TEST_TWB_FILE = os.path.join(
    TEST_ASSET_DIR,
    'group_test.twb'
)

TEST_TWB_FILE2 = os.path.join(
    TEST_ASSET_DIR,
    'datasource_test.twb'
)

ACCESS_PERMISSIONS = os.path.join(
    TEST_ASSET_DIR,
    'access_permissions.csv'
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

class AccessPermissionsTWB(unittest.TestCase):

    def test_user_filter_access_permissions_table(self):
        self.wb = Workbook(TEST_TWB_FILE)
        self.access_permissions = self.wb.access_permissions
        self.group_permissions = self.access_permissions.group_permissions
        self.csv = self.access_permissions.get_permissions_table_CSV()

        self.assertEqual(len(self.group_permissions), 4)
        self.assertEqual(self.group_permissions[0].name, "Jazz Pharmaceuticals-USA-All-Editor")
        self.assertEqual(self.group_permissions[0].advertisers[0], "Jazz Pharma - ADKT Unbranded DTC")
        self.assertEqual(len(self.group_permissions[0].advertisers), 18)
        self.assertEqual(hashlib.sha224(self.csv.encode('UTF-8')).hexdigest(),"78e181dd0e91c7df914b26e71becf92ad93ab5021556a9120151db90")

    def test_csv_access_permissions_table(self):
        with open(ACCESS_PERMISSIONS) as f:
            self.csv2 = f.read()
        self.wb2 = Workbook(TEST_TWB_FILE2)
        self.wb2.ingest_access_permissions(self.csv2)
        self.access_permissions2 = self.wb2.access_permissions
        self.group_permissions2 = self.access_permissions2.group_permissions

        self.assertEqual(len(self.group_permissions2), 4)
        self.assertEqual(self.access_permissions2.get_permissions_table_CSV(), self.csv2)
        self.assertEqual(self.group_permissions2[0].name,'Jazz Pharmaceuticals-USA-All-Editor')
        self.assertEqual(self.group_permissions2[0].advertisers[0],'Jazz Pharma - ADKT Unbranded DTC')
        self.assertEqual(len(self.group_permissions2[0].advertisers), 18)
