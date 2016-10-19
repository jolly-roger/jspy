from js.wrappers.W__PrimitiveObject import W__PrimitiveObject


class W_DateObject(W__PrimitiveObject):
    _class_ = 'Date'

    def default_value(self, hint='String'):
        if hint is None:
            hint = 'String'
        return W_BasicObject.default_value(self, hint)