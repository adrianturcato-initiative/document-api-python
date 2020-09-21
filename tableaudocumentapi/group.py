from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import xml.dom.minidom

class Group(object):
    """A class representing Tableau Zones

    """

    def __init__(self, groupXML):
        """
        Constructor.  Default is to create from xml.

        """
        self._groupXML = groupXML
        self._name = groupXML.get('name', None)
        self._is_user_filter = self._prepare_is_user_filter()

    # xml_string = tostring(self._groupXML)
    # print(xml.dom.minidom.parseString(xml_string).toprettyxml())

    @property
    def groupXML(self):
        return self._groupXML

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._groupXML.set('name', value)

    @property
    def is_user_filter(self):
        return self._is_user_filter

    def _prepare_is_user_filter(self):
        if 'User Filter' in self._name:
            return True
        else:
            return False


