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

class WorksheetTWB(unittest.TestCase):

    def test_shared_views(self):
        self.wb = Workbook(TEST_TWB_FILE)
        self.shared_views = self.wb.shared_views

        self.assertEqual('federated.1cfcaj20zwyr8f1c3we6w0yu3sh4',self.shared_views[0].name)
        self.assertEqual('[federated.1cfcaj20zwyr8f1c3we6w0yu3sh4].[none:Tactic/Targeting (copy):nk]', self.shared_views[0].filters[-1].column)
        self.shared_views[0].addFilter('federated.1cfcaj20zwyr8f1c3we6w0yu3sh4')
        self.assertEqual('[federated.1cfcaj20zwyr8f1c3we6w0yu3sh4].[User Filter 1]', self.shared_views[0].filters[0].column)
