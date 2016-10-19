from js.wrappers.W_BasicObject import W_BasicObject


class W__PrimitiveObject(W_BasicObject):
    _immutable_fields_ = ['_primitive_value_']

    def __init__(self, primitive_value):
        W_BasicObject.__init__(self)
        self.set_primitive_value(primitive_value)

    def PrimitiveValue(self):
        return self._primitive_value_

    def set_primitive_value(self, value):
        assert isinstance(value, W_Root)
        self._primitive_value_ = value