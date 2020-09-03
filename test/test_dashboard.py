import os.path
import unittest


from tableaudocumentapi import Workbook

TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)

TEST_TWB_FILE = os.path.join(
    TEST_ASSET_DIR,
    'dashboard_test.twb'
)

class DashboardTWB(unittest.TestCase):

    def setUp(self):
        self.wb = Workbook(TEST_TWB_FILE)
        # Assume the first datasource in the file
        self.db = self.wb.dashboards[0]

    def test_dashboard_in_workbook(self):
        self.assertIsNotNone(self.db)
        self.assertIsNotNone(self.db.zones)
        self.assertIsNotNone(self.db.logo_zones)
