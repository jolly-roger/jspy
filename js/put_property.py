from js.property_descriptor import PropertyDescriptor


def put_property(obj, name, value, writable=False, configurable=False, enumerable=False, throw=False):
    descriptor = PropertyDescriptor(value=value, writable=writable, configurable=configurable, enumerable=enumerable)
    obj.define_own_property(name, descriptor, throw)