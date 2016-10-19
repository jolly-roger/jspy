from js.wrappers._w import _w
from js.wrappers.W__PrimitiveObject import W__PrimitiveObject
from js.wrappers.W__Array import is_array_index

from js.property_descriptor import PropertyDescriptor


class W_StringObject(W__PrimitiveObject):
    _class_ = 'String'

    def __init__(self, primitive_value):
        W__PrimitiveObject.__init__(self, primitive_value)
        length = len(self._primitive_value_.to_string())
        descr = PropertyDescriptor(value=_w(length), enumerable=False, configurable=False, writable=False)
        self.define_own_property(u'length', descr)

    def get_own_property(self, p):
        desc = W__PrimitiveObject.get_own_property(self, p)
        if desc is not None:
            return desc

        if not is_array_index(p):
            return None

        string = self.to_string()
        index = int(p)
        length = len(string)

        if length <= index:
            return None

        result_string = string[index]
        d = PropertyDescriptor(value=_w(result_string), enumerable=True, writable=False, configurable=False)
        return d