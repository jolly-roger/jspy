from rpython.rlib import jit

from js.wrappers.string import W_String
from js.wrappers.floatNumber import W_FloatNumber
from js.wrappers.boolean import W_Boolean


def isstr(w):
    return isinstance(w, W_String)

def newstring(s):
    return W_String(s)

def _makebool(b):
    return W_Boolean(b)

w_True = _makebool(True)
jit.promote(w_True)


w_False = _makebool(False)
jit.promote(w_False)


def isnull_or_undefined(obj):
    if isnull(obj) or isundefined(obj):
        return True
    return False


def newbool(val):
    if val:
        return w_True
    return w_False


def w_return(fn):
    def f(*args):
        return _w(fn(*args))
    return f
