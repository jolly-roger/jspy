from js.wrappers.primitive import W_Primitive


class W_Boolean(W_Primitive):
    _type_ = 'boolean'
    _immutable_fields_ = ['_boolval_']

    def __init__(self, boolval):
        self._boolval_ = bool(boolval)

    def __str__(self):
        return 'W_Bool(%s)' % (str(self._boolval_), )

    def ToObject(self):
        return object_space.new_bool(self)

    def to_string(self):
        if self._boolval_ is True:
            return u'true'
        return u'false'

    def ToNumber(self):
        if self._boolval_ is True:
            return 1.0
        return 0.0

    def to_boolean(self):
        return self._boolval_


def _makebool(b):
    return W_Boolean(b)

w_True = _makebool(True)

w_False = _makebool(False)

def newbool(val):
    if val:
        return w_True
    return w_False