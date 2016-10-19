from js.wrappers._w import _w
from js.wrappers.null import newnull


class ObjectSpace(object):
    def __init__(self):
        self.global_context = None
        self.global_object = None
        self.proto_function = newnull()
        self.proto_boolean = newnull()
        self.proto_number = newnull()
        self.proto_string = newnull()
        self.proto_array = newnull()
        self.proto_date = newnull()
        self.proto_object = newnull()
        self.interpreter = None

    def get_global_environment(self):
        return self.global_context.variable_environment()

    def assign_proto(self, obj, proto=None):
        if proto is not None:
            obj._prototype_ = proto
            return obj

        if isinstance(obj, W_BasicFunction):
            obj._prototype_ = self.proto_function
        elif isinstance(obj, W_BooleanObject):
            obj._prototype_ = self.proto_boolean
        elif isinstance(obj, W_NumericObject):
            obj._prototype_ = self.proto_number
        elif isinstance(obj, W_StringObject):
            obj._prototype_ = self.proto_string
        elif isinstance(obj, W__Array):
            obj._prototype_ = self.proto_array
        elif isinstance(obj, W_DateObject):
            obj._prototype_ = self.proto_date
        else:
            obj._prototype_ = self.proto_object
        return obj

    def new_obj(self):
        obj = W__Object()
        self.assign_proto(obj)
        return obj

    def new_func(self, function_body, formal_parameter_list=[], scope=None, strict=False):
        obj = W__Function(function_body, formal_parameter_list, scope, strict)
        self.assign_proto(obj)
        return obj

    def new_date(self, value):
        obj = W_DateObject(value)
        self.assign_proto(obj)
        return obj

    def new_array(self, length=_w(0)):
        obj = W__Array(length)
        self.assign_proto(obj)
        return obj

    def new_bool(self, value):
        obj = W_BooleanObject(value)
        self.assign_proto(obj)
        return obj

    def new_string(self, value):
        obj = W_StringObject(value)
        self.assign_proto(obj)
        return obj

    def new_number(self, value):
        obj = W_NumericObject(value)
        self.assign_proto(obj)
        return obj


object_space = ObjectSpace()