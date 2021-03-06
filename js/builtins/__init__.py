from js.put_property import put_property

from js.builtins.object_space import object_space

from js.wrappers._w import _w
from js.wrappers.W__Function import W__Function
from js.wrappers.W_BasicObject import W_BasicObject
from js.wrappers.W_FunctionConstructor import W_FunctionConstructor
from js.wrappers.W_ObjectConstructor import W_ObjectConstructor
from js.wrappers.undefined import newundefined

def new_native_function(function, name=u'', params=[]):
    from js.functions import JsNativeFunction

    jsfunc = JsNativeFunction(function, name)
    obj = W__Function(jsfunc, formal_parameter_list=params)
    return obj

def put_native_function(obj, name, func, writable=True, configurable=True, enumerable=False, params=[]):
    jsfunc = new_native_function(func, name, params)
    put_property(obj, name, jsfunc, writable=writable, configurable=configurable, enumerable=enumerable)

def put_intimate_function(obj, name, func, writable=True, configurable=True, enumerable=False, params=[]):
    from js.functions import JsIntimateFunction

    jsfunc = JsIntimateFunction(func, name)
    w_func = W__Function(jsfunc, formal_parameter_list=params)
    put_property(obj, name, w_func, writable=writable, configurable=configurable, enumerable=enumerable)


def setup_builtins(global_object):
    w_ObjectPrototype = W_BasicObject()
    object_space.proto_object = w_ObjectPrototype
    w_Function = W_FunctionConstructor()
    put_property(global_object, u'Function', w_Function)

    from js.functions import JsNativeFunction

    import js.builtins.function
    empty_func = JsNativeFunction(js.builtins.function.empty, u'Empty')
    w_FunctionPrototype = W__Function(empty_func)
    object_space.assign_proto(w_FunctionPrototype, object_space.proto_object)
    object_space.proto_function = w_FunctionPrototype

    object_space.assign_proto(w_Function, object_space.proto_function)

    w_Object = W_ObjectConstructor()
    object_space.assign_proto(w_Object, object_space.proto_function)

    put_property(w_Object, u'length', _w(1))
    put_property(global_object, u'Object', w_Object)
    put_property(w_Object, u'prototype', w_ObjectPrototype, writable=False, configurable=False, enumerable=False)
    put_property(w_ObjectPrototype, u'constructor', w_Object)

    import js.builtins.object
    put_native_function(w_ObjectPrototype, u'toString', js.builtins.object.to_string)
    put_native_function(w_ObjectPrototype, u'toLocaleString', js.builtins.object.to_string)
    put_native_function(w_ObjectPrototype, u'valueOf', js.builtins.object.value_of)

    put_property(w_Function, u'prototype', w_FunctionPrototype, writable=False, configurable=False, enumerable=False)
    put_property(w_Function, u'length', _w(1), writable=False, configurable=False, enumerable=False)
    put_property(w_FunctionPrototype, u'constructor', w_Function)

    put_native_function(w_FunctionPrototype, u'toString', js.builtins.function.to_string)

    put_intimate_function(w_FunctionPrototype, u'apply', js.builtins.function.js_apply)
    put_intimate_function(w_FunctionPrototype, u'call', js.builtins.function.js_call)

    from js.builtins import jsBoolean, jsNumber, jsString, jsArray, jsMath, jsMath, jsConsole, jsDate, jsGlobal
    jsBoolean.setup(global_object)
    jsNumber.setup(global_object)
    jsString.setup(global_object)
    jsArray.setup(global_object)
    jsMath.setup(global_object)
    jsConsole.setup(global_object)
    jsDate.setup(global_object)
    jsGlobal.setup(global_object)


def get_arg(args, index, default=newundefined()):
    if len(args) > index:
        return args[index]
    return default
