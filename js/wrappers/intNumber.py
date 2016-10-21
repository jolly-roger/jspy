from js.wrappers.number import W_Number


class W_IntNumber(W_Number):
    _immutable_fields_ = ['_intval_']

    """ Number known to be an integer
    """
    def __init__(self, intval):
        self._intval_ = intval

    def __str__(self):
        return 'W_IntNumber(%s)' % (self._intval_,)

    def ToInteger(self):
        return self._intval_

    def ToNumber(self):
        # XXX
        return float(self._intval_)

    def to_string(self):
        # XXX incomplete, this doesn't follow the 9.8.1 recommendation
        return unicode(str(self.ToInteger()))

def newint(i):
    return W_IntNumber(i)

def isint(w):
    return isinstance(w, W_IntNumber)