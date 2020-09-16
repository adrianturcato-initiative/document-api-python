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

class GroupTWB(unittest.TestCase):

    def setUp(self):
        self.wb = Workbook(TEST_TWB_FILE)
        # Assume the first datasource in the file
        self.db = self.wb.dashboards[0]
        self.zone = self.db.zones[0]
        self.logo_zone = self.db.logo_zones[0]

    def test_groups_in_dashboard(self):
        self.assertIsNotNone(self.zone)
        self.assertIsNotNone(self.logo_zone)



