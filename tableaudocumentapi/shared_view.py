from xml.etree.ElementTree import Element, SubElement, tostring

class Filter(object):
    def __init__(self, filterXML):
        self._filterXML = filterXML
        self._column = self._filterXML.attrib['column']

    @property
    def column(self):
        return self._column

class SharedView(object):
    def __init__(self, sharedViewXML):
        self._sharedViewXML = sharedViewXML
        self._name = sharedViewXML.attrib['name']
        self._datasources = self._prepare_datasources(self._sharedViewXML)
        self._filters = self._prepare_filters(self._sharedViewXML)

    @property
    def datasources(self):
        return self._datasources

    @property
    def name(self):
        return self._name

    @property
    def filters(self):
        return self._filters

    def addFilter(self,datasource_name):
        filter_el = Element('filter',column=f"[{datasource_name}].[User Filter 1]",context='true')
        filter_el.set('class','categorical') #attribute name include special term so we will set in a different fashion
        self._sharedViewXML.insert(2,filter_el)
        self._filters = self._prepare_filters(self._sharedViewXML)

    @staticmethod
    def _prepare_filters(sharedViewXML):
        return [Filter(f) for f in sharedViewXML.findall('.//filter')]

    @staticmethod
    def _prepare_datasources(sharedViewXML):
        return [d.attrib for d in sharedViewXML.findall('.//datasource')]