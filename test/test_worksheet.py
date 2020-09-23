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

ACCESS_PERMISSIONS = os.path.join(
    TEST_ASSET_DIR,
    'access_permissions.csv'
)

class WorksheetTWB(unittest.TestCase):

    def test_worksheet(self):
        self.wb = Workbook(TEST_TWB_FILE)
        self.worksheets = self.wb.worksheets

        self.assertEqual('federated.1cfcaj20zwyr8f1c3we6w0yu3sh4',self.worksheets[0].datasources[0]['name'])
        self.assertTrue(self.worksheets[0].slices.has_user_filter())


    def test_adding_column_to_slices(self):
        print("test_adding_column_to_slices")
        with open(ACCESS_PERMISSIONS) as f:
            self.csv2 = f.read()
        self.wb2 = Workbook(TEST_TWB_FILE2)

        self.assertEqual(2,len(self.wb2.worksheets))
        self.assertEqual('Sheet 1', self.wb2.worksheets[0].name)
        self.assertEqual('[federated.1cfcaj20zwyr8f1c3we6w0yu3sh4].[none:Advertiser:nk]', self.wb2.worksheets[0].slices.columns[0])
        self.assertFalse(self.wb2.worksheets[0].slices.has_user_filter())

        self.wb2.ingest_access_permissions('federated.1cfcaj20zwyr8f1c3we6w0yu3sh4',self.csv2)

        self.assertEqual("[federated.1cfcaj20zwyr8f1c3we6w0yu3sh4].[User Filter 1]",self.wb2.worksheets[0].slices.columns[0])
        self.assertTrue("has", self.wb2.worksheets[0].slices.has_user_filter())
