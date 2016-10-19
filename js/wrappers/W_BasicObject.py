from js.object_map import new_map
from js.property_descriptor import AccessorPropertyDescriptor, is_generic_descriptor, is_data_descriptor, is_accessor_descriptor
from js.property import AccessorProperty, DataProperty

from js.wrappers.root import W_Root
from js.wrappers.null import newnull
from js.wrappers.W_ProtoGetter import W_ProtoGetter
from js.wrappers.W_ProtoSetter import W_ProtoSetter


w_proto_getter = W_ProtoGetter()
w_proto_setter = W_ProtoSetter()
proto_desc = AccessorPropertyDescriptor(w_proto_getter, w_proto_setter, False, False)


class W_BasicObject(W_Root):
    _type_ = 'object'
    _class_ = 'Object'
    _extensible_ = True
    _immutable_fields_ = ['_type_', '_class_']  # TODO why need _primitive_value_ here???

    def __init__(self):
        self._property_map_ = new_map()
        self._property_slots_ = []

        self._prototype_ = newnull()
        W_BasicObject.define_own_property(self, u'__proto__', proto_desc)

    def __str__(self):
        return "%s: %s" % (object.__repr__(self), self.klass())

    ##########
    # 8.6.2 Object Internal Properties and Methods
    def prototype(self):
        return self._prototype_

    def klass(self):
        return self._class_

    def extensible(self):
        return self._extensible_

    # 8.12.3
    def get(self, p):
        assert p is not None and isinstance(p, unicode)
        desc = self.get_property(p)

        return _get_from_desc(desc, self)

    def w_get(self, w_p):
        name = w_p.to_string()
        return self.get(name)

    # 8.12.1
    def get_own_property(self, p):
        assert p is not None and isinstance(p, unicode)

        prop = self._get_prop(p)
        if prop is None:
            return

        return prop.to_property_descriptor()

    def _get_prop(self, name):
        idx = self._property_map_.lookup(name)

        if self._property_map_.not_found(idx):
            return

        prop = self._property_slots_[idx]
        return prop

    def _del_prop(self, name):
        idx = self._property_map_.lookup(name)

        if self._property_map_.not_found(idx):
            return

        assert idx >= 0
        self._property_slots_ = self._property_slots_[:idx] + self._property_slots_[idx + 1:]
        self._property_map_ = self._property_map_.delete(name)

    def _add_prop(self, name, value):
        idx = self._property_map_.lookup(name)

        if self._property_map_.not_found(idx):
            self._property_map_ = self._property_map_.add(name)
            idx = self._property_map_.index

        if idx >= len(self._property_slots_):
            self._property_slots_ = self._property_slots_ + ([None] * (1 + idx - len(self._property_slots_)))

        self._property_slots_[idx] = value

    def _set_prop(self, name, value):
        idx = self._property_map_.lookup(name)
        self._property_slots_[idx] = value

    # 8.12.2
    def get_property(self, p):
        assert p is not None and isinstance(p, unicode)

        prop = self.get_own_property(p)
        if prop is not None:
            return prop

        proto = self.prototype()
        if isnull(proto):
            return None

        assert isinstance(proto, W_BasicObject)
        return proto.get_property(p)

    # 8.12.5
    def put(self, p, v, throw=False):
        assert p is not None and isinstance(p, unicode)

        if not self.can_put(p):
            if throw:
                raise JsTypeError(u"can't put %s" % (p, ))
            else:
                return

        own_desc = self.get_own_property(p)
        if is_data_descriptor(own_desc) is True:
            value_desc = PropertyDescriptor(value=v)
            self.define_own_property(p, value_desc, throw)
            return

        desc = self.get_property(p)
        if is_accessor_descriptor(desc) is True:
            setter = desc.setter
            assert setter is not None
            setter.Call(this=self, args=[v])
        else:
            new_desc = DataPropertyDescriptor(v, True, True, True)
            self.define_own_property(p, new_desc, throw)

    def w_put(self, w_p, v, throw=False):
        name = w_p.to_string()
        self.put(name, v, throw)

    def can_put(self, p):
        desc = self.get_own_property(p)
        if desc is not None:
            if is_accessor_descriptor(desc) is True:
                if isundefined(desc.setter):
                    return False
                else:
                    return True
            return desc.writable

        proto = self.prototype()

        if isnull_or_undefined(proto):
            return self.extensible()

        assert isinstance(proto, W_BasicObject)
        inherited = proto.get_property(p)
        if inherited is None:
            return self.extensible()

        if is_accessor_descriptor(inherited) is True:
            if isundefined(inherited.setter):
                return False
            else:
                return True
        else:
            if self.extensible() is False:
                return False
            else:
                return inherited.writable

    # 8.12.6
    def has_property(self, p):
        assert p is not None and isinstance(p, unicode)

        desc = self.get_property(p)
        if desc is None:
            return False
        return True

    # 8.12.7
    def delete(self, p, throw=False):
        desc = self.get_own_property(p)
        if desc is None:
            return True
        if desc.configurable:
            self._del_prop(p)
            return True

        if throw is True:
            raise JsTypeError(u'')

        return False

    # 8.12.8
    def default_value(self, hint='Number'):
        if hint == 'String':
            res = self._default_value_string_()
            if res is None:
                res = self._default_value_number_()
        else:
            res = self._default_value_number_()
            if res is None:
                res = self._default_value_string_()

        if res is not None:
            return res

        raise JsTypeError(u'')

    def _default_value_string_(self):
        to_string = self.get(u'toString')

        if to_string.is_callable():
            assert isinstance(to_string, W_BasicFunction)
            _str = to_string.Call(this=self)
            if isinstance(_str, W_Primitive):
                return _str

    def _default_value_number_(self):
        value_of = self.get(u'valueOf')
        if value_of.is_callable():
            assert isinstance(value_of, W_BasicFunction)
            val = value_of.Call(this=self)
            if isinstance(val, W_Primitive):
                return val

    # 8.12.9
    def define_own_property(self, p, desc, throw=False):
        current = self.get_own_property(p)
        extensible = self.extensible()

        # 3.
        if current is None and extensible is False:
            return reject(throw, p)

        # 4.
        if current is None and extensible is True:
            # 4.a
            if is_generic_descriptor(desc) or is_data_descriptor(desc):
                new_prop = DataProperty(
                    desc.value,
                    desc.writable,
                    desc.enumerable,
                    desc.configurable
                )
                self._add_prop(p, new_prop)
            # 4.b
            else:
                assert is_accessor_descriptor(desc) is True
                new_prop = AccessorProperty(
                    desc.getter,
                    desc.setter,
                    desc.enumerable,
                    desc.configurable
                )
                self._add_prop(p, new_prop)
            # 4.c
            return True

        # 5.
        if desc.is_empty():
            return True

        # 6.
        if desc == current:
            return True

        # 7.
        if current.configurable is False:
            if desc.configurable is True:
                return reject(throw, p)
            if desc.has_set_enumerable() and (not(current.enumerable) == desc.enumerable):
                return reject(throw, p)

        # 8.
        if is_generic_descriptor(desc):
            pass
        # 9.
        elif is_data_descriptor(current) != is_data_descriptor(desc):
            # 9.a
            if current.configurable is False:
                return reject(throw, p)
            # 9.b
            if is_data_descriptor(current):
                raise NotImplementedError(self.__class__)
            # 9.c
            else:
                raise NotImplementedError(self.__class__)
        # 10
        elif is_data_descriptor(current) and is_data_descriptor(desc):
            # 10.a
            if current.configurable is False:
                # 10.a.i
                if current.writable is False and desc.writable is True:
                    return reject(throw, p)
                # 10.a.ii
                if current.writable is False:
                    if desc.has_set_value() and desc.value != current.value:
                        return reject(throw, p)
            # 10.b
            else:
                pass
        # 11
        elif is_accessor_descriptor(current) and is_accessor_descriptor(desc):
            # 11.a
            if current.configurable is False:
                # 11.a.i
                if desc.has_set_setter() and desc.setter != current.setter:
                    return reject(throw, p)
                # 11.a.ii
                if desc.has_set_getter() and desc.getter != current.getter:
                    return reject(throw, p)
        # 12
        prop = self._get_prop(p)
        prop.update_with_descriptor(desc)

        # 13
        return True

    ##########
    def to_boolean(self):
        return True

    def ToNumber(self):
        return self.ToPrimitive('Number').ToNumber()

    def to_string(self):
        return self.ToPrimitive('String').to_string()

    def ToPrimitive(self, hint=None):
        return self.default_value(hint)

    def ToObject(self):
        return self

    def has_instance(self, other):
        raise JsTypeError(u'has_instance')
    ###

    def _named_properties_dict(self):
        my_d = {}
        for i in self._property_map_.keys():
            my_d[i] = None

        proto = self.prototype()
        if not isnull_or_undefined(proto):
            assert isinstance(proto, W_BasicObject)
            proto_d = proto._named_properties_dict()
        else:
            proto_d = {}

        my_d.update(proto_d)

        return my_d

    def named_properties(self):
        prop_dict = self._named_properties_dict()
        return prop_dict.keys()
