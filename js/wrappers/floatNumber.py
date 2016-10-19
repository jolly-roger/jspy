from js.wrappers.number import W_Number


class W_FloatNumber(W_Number):
    _immutable_fields_ = ['_floatval_']

    """ Number known to be a float
    """
    def __init__(self, floatval):
        assert isinstance(floatval, float)
        self._floatval_ = floatval

    def __str__(self):
        return 'W_FloatNumber(%s)' % (self._floatval_,)

    def to_string(self):
        # XXX incomplete, this doesn't follow the 9.8.1 recommendation
        if isnan(self._floatval_):
            return u'NaN'
        if isinf(self._floatval_):
            if self._floatval_ > 0:
                return u'Infinity'
            else:
                return u'-Infinity'

        if self._floatval_ == 0:
            return u'0'

        res = u''
        try:
            res = unicode(formatd(self._floatval_, 'g', 10))
        except OverflowError:
            raise

        if len(res) > 3 and (res[-3] == '+' or res[-3] == '-') and res[-2] == '0':
            cut = len(res) - 2
            assert cut >= 0
            res = res[:cut] + res[-1]
        return res

    def ToNumber(self):
        return self._floatval_

    def ToInteger(self):
        if isnan(self._floatval_):
            return 0

        if self._floatval_ == 0 or isinf(self._floatval_):
            return int(self._floatval_)

        return intmask(int(self._floatval_))


def isfloat(w):
    return isinstance(w, W_FloatNumber)

def newfloat(f):
    return W_FloatNumber(f)