import weakref
from xml.etree.ElementTree import Element, SubElement

from tableaudocumentapi import Datasource, Dashboard, xfile, AccessPermissions
from tableaudocumentapi.xfile import xml_open


class Workbook(object):
    """A class for writing Tableau workbook files."""

    def __init__(self, filename):
        """Open the workbook at `filename`. This will handle packaged and unpacked
        workbook files automatically. This will also parse Data Sources and Worksheets
        for access.

        """

        self._filename = filename

        self._name = self._prepare_name(self._filename)

        self._workbookTree = xml_open(self._filename, 'workbook')

        self._workbookRoot = self._workbookTree.getroot()
        # prepare our datasource objects
        self._datasources = self._prepare_datasources(self._workbookRoot)

        self._datasource_index = self._prepare_datasource_index(self._datasources)

        self._worksheets = self._prepare_worksheets(self._workbookRoot, self._datasource_index)

        self._dashboards = self._prepare_dashboards(self._workbookRoot)

        self._user_filter = self._prepare_user_filter(self._datasources)

        self._access_permissions = self._prepare_access_permissions(self._user_filter)

    @property
    def datasources(self):
        return self._datasources

    @property
    def dashboards(self):
        return self._dashboards

    @property
    def worksheets(self):
        return self._worksheets

    @property
    def filename(self):
        return self._filename

    @property
    def name(self):
        return self._name

    @property
    def user_filter(self):
        return self._user_filter

    @property
    def access_permissions(self):
        return self._access_permissions

    def save(self):
        """
        Call finalization code and save file.

        Args:
            None.

        Returns:
            Nothing.

        """

        # save the file
        xfile._save_file(self._filename, self._workbookTree)

    def save_as(self, new_filename, new_logo=None):
        """
        Save our file with the name provided.

        Args:
            new_filename:  New name for the workbook file. String.

        Returns:
            Nothing.

        """
        xfile._save_file(self._filename, self._workbookTree, new_filename, new_logo)

    @staticmethod
    def _prepare_datasource_index(datasources):
        retval = weakref.WeakValueDictionary()
        for datasource in datasources:
            retval[datasource.name] = datasource

        return retval

    @staticmethod
    def _prepare_datasources(xml_root):
        datasources = []

        # loop through our datasources and append
        datasource_elements = xml_root.find('datasources')
        if datasource_elements is None:
            return []

        for datasource in datasource_elements:
            ds = Datasource(datasource)
            datasources.append(ds)

        return datasources

    @staticmethod
    def _prepare_worksheets(xml_root, ds_index):
        worksheets = []
        worksheets_element = xml_root.find('.//worksheets')
        if worksheets_element is None:
            return worksheets

        for worksheet_element in worksheets_element:
            worksheet_name = worksheet_element.attrib['name']
            worksheets.append(worksheet_name)  # TODO: A real worksheet object, for now, only name
            dependencies = worksheet_element.findall('.//datasource-dependencies')

            for dependency in dependencies:
                datasource_name = dependency.attrib['datasource']
                datasource = ds_index[datasource_name]
                for column in dependency.findall('.//column'):
                    column_name = column.attrib['name']
                    if column_name in datasource.fields:
                        datasource.fields[column_name].add_used_in(worksheet_name)

        return worksheets

    @staticmethod
    def _prepare_dashboards(xml_root):
        dashboards = []

        # loop through our datasources and append
        dashboard_elements = xml_root.find('dashboards')
        if dashboard_elements is None:
            return []

        for dashboard in dashboard_elements:
            db = Dashboard(dashboard)
            dashboards.append(db)

        return dashboards

    @staticmethod
    def _prepare_name(filename):
        f = filename.split("\\")[-1].split(".")[0]
        return f

    @staticmethod
    def _prepare_user_filter(datasources):
        print("_prepare_user_filter")
        for i, d in enumerate(datasources):
            groups = d.groups
            for j, g in enumerate(groups):
                if g.is_user_filter:
                    return g
        return None

    @staticmethod
    def _prepare_access_permissions(user_filter):
        if user_filter:
            return AccessPermissions(user_filter_group=user_filter)
        else:
            return None

    def ingest_access_permissions(self,csv):
        self._access_permissions = AccessPermissions(csv_file_contents=csv)

    @staticmethod
    def _get_user_filter_parent_datasource(datasources):
        print("_prepare_user_filter")
        for i, d in enumerate(datasources):
            groups = d.groups
            for j, g in enumerate(groups):
                if g.is_user_filter:
                    return d
        return None

    def insert_user_filter(self):
        pass


