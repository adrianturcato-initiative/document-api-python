from tableaudocumentapi import Zone

class Dashboard(object):
    """A class representing Tableau Dashboards, embedded in workbook files

    """

    def __init__(self, xml):
        """
        Constructor.  Default is to create from xml.

        """
        self._dashboardXML = xml
        self._zones = self._prepare_zones(xml)
        self._logo_zones = self._prepare_logo_zones()

    @staticmethod
    def _prepare_zones(xml):
        zones = []

        # loop through our datasources and append
        zone_elements = xml.find('zones')
        if zone_elements is None:
            return []

        for zone in zone_elements:
            zn = Zone(zone)
            zones.append(zn)
        return zones

    def _prepare_logo_zones(self):
        logo_zones = []
        for zone in self._zones:
            if zone.type == 'bitmap':
                logo_zones.append(zone)

        return logo_zones

    @property
    def logo_zones(self):
        return self._logo_zones
