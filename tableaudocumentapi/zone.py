class Zone(object):
    """A class representing Tableau Zones

    """

    def __init__(self, xml):
        """
        Constructor.  Default is to create from xml.

        """
        self._zoneXML = xml
        self._id = xml.get('id', None)
        self._name = xml.get('name', None)
        self._type = xml.get('type', None)
        self._param = xml.get('param', None)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        self._zoneXML.set('id', value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._zoneXML.set('name', value)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
        self._zoneXML.set('type', value)

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, value):
        self._param = value
        self._zoneXML.set('param', value)

