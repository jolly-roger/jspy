from js.wrappers.primitive import W_Primitive


class W_Undefined(W_Primitive):
    _type_ = 'undefined'

    def ToInteger(self):
        return 0

    def ToNumber(self):
        return NAN

    def to_string(self):
        return unicode(self._type_)

    def check_object_coercible(self):
        raise JsTypeError(u'W_Undefined.check_object_coercible')

    def ToObject(self):
        raise JsTypeError(u'W_Undefined.ToObject')


def isundefined(value):
    return value is W_Undefined


def newundefined():
    return W_Undefined