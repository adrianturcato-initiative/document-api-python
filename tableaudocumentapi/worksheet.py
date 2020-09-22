from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import xml.dom.minidom

class Slices(object):
    def __init__(self, slicesXML):
        """
        Constructor.  Default is to create from xml.

        """
        self._slicesXML = slicesXML
        self._columns = self._prepare_columns(slicesXML)

    @property
    def columns(self):
        return self._columns

    def addColumn(self,contents):
        column = SubElement(self._slicesXML,'column')
        column.text = contents
        self._columns = self._prepare_columns(self._slicesXML)

    def has_user_filter(self):
        for c in self._columns:
            if 'User Filter' in c:
                return True
        return False

    @staticmethod
    def _prepare_columns(slicesXML):
        return [c.text for c in slicesXML.findall('.//column')]

class Worksheet(object):
    """A class representing Tableau Zones

    """

    def __init__(self, worksheetXML):
        """
        Constructor.  Default is to create from xml.

        """
        self._worksheetXML = worksheetXML
        self._name = worksheetXML.attrib['name']
        self._datasources = self._prepare_datasources(worksheetXML)
        self._slices = self._prepare_slices(worksheetXML)

    @property
    def name(self):
        return self._name

    @property
    def datasources(self):
        return self._datasources

    @property
    def slices(self):
        return self._slices

    @staticmethod
    def _prepare_datasources(worksheetXML):
        return [d.attrib for d in worksheetXML.findall('.//datasource')]

    @staticmethod
    def _prepare_slices(worksheetXML):
        sliceXML = worksheetXML.find('.//slices')
        if sliceXML:
            return Slices(sliceXML)
        else:
            return None

