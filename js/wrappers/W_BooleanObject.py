from js.wrappers.W__PrimitiveObject import W__PrimitiveObject


class W_BooleanObject(W__PrimitiveObject):
    _class_ = 'Boolean'

    def __str__(self):
        return u'W_BooleanObject(%s)' % (str(self._primitive_value_))