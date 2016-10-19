from js.wrappers.primitive import W_Primitive


class W_Null(W_Primitive):
    _type_ = 'null'

    def to_boolean(self):
        return False

    def to_string(self):
        return u'null'

    def check_object_coercible(self):
        raise JsTypeError(u'W_Null.check_object_coercible')

    def ToObject(self):
        raise JsTypeError(u'W_Null.ToObject')


def isnull(value):
    return value is W_Null

def newnull():
    return W_Null