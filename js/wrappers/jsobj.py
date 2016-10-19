# encoding: utf-8
from rpython.rlib.rfloat import isnan, isinf, NAN, formatd, INFINITY
from rpython.rlib.objectmodel import enforceargs
from rpython.rlib import jit, debug

from js.property_descriptor import PropertyDescriptor, DataPropertyDescriptor, AccessorPropertyDescriptor, is_data_descriptor, \
    is_generic_descriptor, is_accessor_descriptor
from js.property import DataProperty, AccessorProperty
from js.object_map import new_map
from js.exception import JsTypeError, JsRangeError
from js.object_space import isnull_or_undefined
from js.builtins import get_arg
from js.astbuilder import parse_to_ast
from js.jscode import ast_to_bytecode
from js.execution_context import FunctionExecutionContext
from js.completion import Completion
from js.builtins.jsGlobal import _strip, _parse_int
from js.runistr import encode_unicode_utf8
from js.constants import hex_rexp, oct_rexp, num_rexp

from js.wrappers.root import W_Root
from js.wrappers.undefined import newundefined, isundefined
from js.wrappers.null import newnull, isnull


@jit.elidable
def is_array_index(p):
    return make_array_index(p) != NOT_ARRAY_INDEX


NOT_ARRAY_INDEX = -1


class Descr(object):
    def __init__(self, can_put, own, inherited, prop):
        self.can_put = can_put
        self.own = own
        self.inherited = inherited
        self.prop = prop


def _get_from_desc(desc, this):
    if desc is None:
        return newundefined()

    if is_data_descriptor(desc):
        return desc.value

    if desc.has_set_getter() is False:
        return newundefined()

    getter = desc.getter
    res = getter.Call(this=this)
    return res


@jit.unroll_safe
def make_array_index(idx):
    if len(idx) == 0:
        return -1

    IDX_LIT = '0123456789'

    for c in idx:
        if c not in IDX_LIT:
            return NOT_ARRAY_INDEX
    return int(idx)


@jit.elidable
def sign(i):
    if i > 0:
        return 1
    if i < 0:
        return -1
    return 0


class PropertyIdenfidier(object):
    def __init__(self, name, descriptor):
        self.name = name
        self.descriptor = descriptor


class W_ProtoGetter(W_Root):
    def is_callable(self):
        return True

    def Call(self, args=[], this=None, calling_context=None):
        if not isinstance(this, W_BasicObject):
            raise JsTypeError(u'')

        return this._prototype_


class W_ProtoSetter(W_Root):
    def is_callable(self):
        return True

    def Call(self, args=[], this=None, calling_context=None):
        if not isinstance(this, W_BasicObject):
            raise JsTypeError(u'')

        proto = args[0]
        this._prototype_ = proto

w_proto_getter = W_ProtoGetter()
w_proto_setter = W_ProtoSetter()
proto_desc = AccessorPropertyDescriptor(w_proto_getter, w_proto_setter, False, False)
jit.promote(proto_desc)


def reject(throw, msg=u''):
    if throw:
        raise JsTypeError(msg)
    return False


def _ireject(throw, idx):
    if throw:
        raise JsTypeError(unicode(str(idx)))
    return False


def make_arg_getter(name, env):
    pass
    #code = u'return %s;' % (name)


def make_arg_setter(name, env):
    pass
    #param = u'%s_arg' % (name)
    #code = u'%s = %s;' % (name, param)
