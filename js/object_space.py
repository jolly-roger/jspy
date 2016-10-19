from js.wrappers.string import W_String
from js.wrappers.floatNumber import W_FloatNumber
from js.wrappers.boolean import W_Boolean


def isstr(w):
    return isinstance(w, W_String)

def isnull_or_undefined(obj):
    if isnull(obj) or isundefined(obj):
        return True
    return False


def w_return(fn):
    def f(*args):
        return _w(fn(*args))
    return f
