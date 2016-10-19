from js.wrappers.root import W_Root
from js.wrappers.intNumber import newint
from js.wrappers.floatNumber import newfloat


def _w(value):
    if value is None:
        return newnull()
    elif isinstance(value, W_Root):
        return value
    elif isinstance(value, bool):
        return newbool(value)
    elif isinstance(value, int):
        return newint(value)
    elif isinstance(value, float):
        return newfloat(value)
    elif isinstance(value, unicode):
        return newstring(value)
    elif isinstance(value, str):
        u_str = unicode(value)
        return newstring(u_str)
    elif isinstance(value, list):
        a = object_space.new_array()
        for index, item in enumerate(value):
            put_property(a, unicode(str(index)), _w(item), writable=True, enumerable=True, configurable=True)
        return a

    raise TypeError("ffffuuu %s" % (value,))