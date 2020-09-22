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
    'add_user_filter_test.twb'
)

TEST_SAVES_THIS_FILE = os.path.join(
    TEST_ASSET_DIR,
    'saved_with_user_filter_group_test.twb'
)

ACCESS_PERMISSIONS = os.path.join(
    TEST_ASSET_DIR,
    'access_permissions.csv'
)

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
        self.wb2.ingest_access_permissions('federated.1cfcaj20zwyr8f1c3we6w0yu3sh4',self.csv2)
        self.access_permissions2 = self.wb2.access_permissions
        self.group_permissions2 = self.access_permissions2.group_permissions

        self.assertEqual(4,len(self.group_permissions2))
        self.assertEqual(self.access_permissions2.get_permissions_table_CSV(), self.csv2)
        self.assertEqual('Jazz Pharmaceuticals-USA-All-Editor',self.group_permissions2[0].name)
        self.assertEqual('Jazz Pharma - ADKT Unbranded DTC',self.group_permissions2[0].advertisers[0])
        self.assertEqual(18,len(self.group_permissions2[0].advertisers))

        self.wb2.save_as(TEST_SAVES_THIS_FILE)

        self.wb3 = Workbook(TEST_SAVES_THIS_FILE)
        self.access_permissions3 = self.wb3.access_permissions
        self.group_permissions3 = self.access_permissions3.group_permissions
        self.csv3 = self.access_permissions3.get_permissions_table_CSV()

        self.assertEqual(4,len(self.group_permissions3))
        self.assertEqual("Jazz Pharmaceuticals-USA-All-Editor",self.group_permissions3[0].name)
        self.assertEqual("Jazz Pharma - ADKT Unbranded DTC",self.group_permissions3[0].advertisers[0])
        self.assertEqual(18,len(self.group_permissions3[0].advertisers))
        self.assertEqual(hashlib.sha224(self.csv3.encode('UTF-8')).hexdigest(),"78e181dd0e91c7df914b26e71becf92ad93ab5021556a9120151db90")