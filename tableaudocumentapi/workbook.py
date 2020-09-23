import weakref
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

from tableaudocumentapi import Datasource, Dashboard, xfile, AccessPermissions, Worksheet, SharedView
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

        self._shared_views = self._prepare_shared_views(self._workbookRoot)

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

    @property
    def shared_views(self):
        return self._shared_views

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
            worksheets.append(Worksheet(worksheet_element))
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
        for i, d in enumerate(datasources):
            groups = d.groups
            for j, g in enumerate(groups):
                if g.is_user_filter:
                    # xml_string = tostring(d._datasourceXML)
                    # print(xml.dom.minidom.parseString(xml_string).toprettyxml())
                    # print(d._datasourceXML.attrib)
                    return g
        return None

    def has_user_filter(self):
        if self._user_filter:
            return True
        else:
            return False

    @staticmethod
    def _prepare_access_permissions(user_filter):
        if user_filter:
            return AccessPermissions(user_filter_group=user_filter)
        else:
            return None

    def ingest_access_permissions(self,datasource_name,csv):
        self._access_permissions = AccessPermissions(csv_file_contents=csv)
        filter_groups = self._access_permissions.group_permissions
        parent_datasource = self._get_user_filter_parent_datasource(datasource_name)
        if parent_datasource:
            parent_XML = parent_datasource.datasourceXML
            self._apply_user_filter_group(parent_XML,filter_groups)
            #add columns to relevant slices
            for worksheet in self._worksheets:
                datasources = worksheet.datasources
                if datasources[0]['name'] == datasource_name:
                    if len(datasources) == 1 or (len(datasources) == 2 and datasources[1]['name'] == 'Parameters'):
                        #TODO check for duplicates?
                        worksheet.slices.addColumn(f"[{datasource_name}].[User Filter 1]")
            #add shared-views filter
            for shared_view in self._shared_views:
                datasources = shared_view.datasources
                if datasources[0]['name'] == datasource_name:
                    if len(datasources) == 1 or (len(datasources) == 2 and datasources[1]['name'] == 'Parameters'):
                        # TODO check for duplicates?
                        shared_view.addFilter(datasource_name)
            #add window viewpoint, what is this, does it matter? only one worksheet has it applied...
        else:
            #TODO proper error handling
            print("ERROR: parent datasource not found")

    def _get_user_filter_parent_datasource(self,datasource_name):
        if self._user_filter:
            for i, d in enumerate(self._datasources):
                groups = d.groups
                for j, g in enumerate(groups):
                    if g.is_user_filter:
                        #TODO overwrite existing user filter group?
                        print("ERROR: duplicate user filter groups created")
                        return d
        else:
            #what group should be the parent of the user filter
            for i, d in enumerate(self._datasources):
                if d.name == datasource_name:
                    return d

    @staticmethod
    def _apply_user_filter_group(parent_XML,filter_groups):
        group_el = Element('group',name='[User Filter 1]')
        group_el.set('name-style','unqualified') #attribute name include special chars so we will set in a different fashion
        group_el.set('user:ui-builder','identity-set') #attribute name include special chars so we will set in a different fashion
        intersection_el = SubElement(group_el, 'groupfilter', function="intersection")
        SubElement(intersection_el, 'groupfilter', function='level-members', level='[Advertiser]' )
        union_el = SubElement(intersection_el, 'groupfilter', function="union")
        union_sub_el = SubElement(union_el, 'groupfilter', expression='false', function='filter')
        SubElement(union_sub_el, 'groupfilter', function='level-members', level='[Advertiser]')

        for grp in filter_groups:
            user_el = SubElement(union_el, 'groupfilter', expression=f"ISMEMBEROF('local\\{grp.name}')", function="filter")
            user_union_el = SubElement(user_el, 'groupfilter', function="union")
            for ad in grp.advertisers:
                SubElement(user_union_el, 'groupfilter', function='member', level='[Advertiser]', member=f'"{ad}"')

        last_group_or_column_index = -1
        for i, el in enumerate(list(parent_XML)):
            if el.tag == 'group' or el.tag == 'column':
                last_group_or_column_index = i

        parent_XML.insert(last_group_or_column_index+1,group_el)

    @staticmethod
    def _prepare_shared_views(xml_root):
        return [SharedView(sv) for sv in xml_root.findall('.//shared-view')]

