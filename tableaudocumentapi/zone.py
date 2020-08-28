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
        self._h = xml.get('h', None)
        self._w = xml.get('w', None)
        self._x = xml.get('x', None)
        self._y = xml.get('y', None)
        self._forceUpdate = xml.get('forceUpdate', None)

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

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self._h = value
        self._zoneXML.set('h', value)

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value
        self._zoneXML.set('w', value)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._zoneXML.set('x', value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._zoneXML.set('y', value)