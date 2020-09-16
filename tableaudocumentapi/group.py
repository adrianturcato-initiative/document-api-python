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
        self._name = xml.get('name', None)

        xml_string = tostring(groupXML)
        print(xml.dom.minidom.parseString(xml_string).toprettyxml())

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._groupXML.set('name', value)

    @classmethod
    def build_user_filter_group(cls):
        group_el = Element('group'
                              ,xmlns="http://www.tableausoftware.com/xml/user"
                              ,name="[User Access]"
                              ,nameStyle="unqualified"
                              ,uiBuilder="identity-set")
        intersection_el = SubElement(group_el, 'groupfilter', function="intersection")
        SubElement(intersection_el, 'groupfilter', function="level-members", level="[Calculation_-6149665274906808319]")
        union_el = SubElement(intersection_el, 'groupfilter', function="union")
        union_sub_el = SubElement(union_el, 'groupfilter', expression='false', function='filter')
        SubElement(union_sub_el, 'groupfilter',function="level-members",level="[Calculation_-6149665274906808319]")

        for user in users:
