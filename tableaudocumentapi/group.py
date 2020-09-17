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

    @classmethod
    def build_user_filter_group(cls,filter_groups):
        group_el = Element('group',name='[User Filter 1]', name_style='unqualified', user_ui_builder='identity-set')
        intersection_el = SubElement(group_el, 'groupfilter', function="intersection")
        SubElement(intersection_el, function='level-members', level='[Advertiser]' )
        union_el = SubElement(intersection_el, 'groupfilter', function="union")
        union_sub_el = SubElement(union_el, 'groupfilter', expression='false', function='filter')
        SubElement(union_sub_el, 'groupfilter',function='level-members', level='[Advertiser]')

        for grp in filter_groups:
            user_el = SubElement(union_el, 'groupfilter', expression=f"ISCURRENTUSER('{grp.name}')", function="filter")
            user_union_el = SubElement(user_el, 'groupfilter', function="union")
            for ad in grp.advertisers:
                SubElement(user_union_el, 'groupfilter', function='member', level='[Advertiser]', member=f'&quot;{ad}&quot;' )

        return group_el