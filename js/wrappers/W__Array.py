from js.wrappers.W_BasicObject import W_BasicObject
from js.wrappers.intNumber import W_IntNumber


w_0 = W_IntNumber(0)

class W__Array(W_BasicObject):
    _class_ = 'Array'

    def __init__(self, length=w_0):
        self._array_props_ = {}
        #self._array_props_ = []

        W_BasicObject.__init__(self)
        assert isinstance(length, W_Root)

        desc = PropertyDescriptor(value=length, writable=True, enumerable=False, configurable=False)
        W_BasicObject.define_own_property(self, u'length', desc)

    ####### dict
    def _add_prop(self, name, value):
        idx = make_array_index(name)
        if idx != NOT_ARRAY_INDEX:
            self._add_iprop(idx, value)
        else:
            W_BasicObject._add_prop(self, name, value)

    def _add_iprop(self, idx, value):
        assert isinstance(idx, int)
        self._array_props_[idx] = value

    def _get_prop(self, name):
        idx = make_array_index(name)
        if idx != NOT_ARRAY_INDEX:
            return self._get_iprop(idx)
        else:
            return W_BasicObject._get_prop(self, name)

    def _get_iprop(self, idx):
        assert isinstance(idx, int)
        assert idx >= 0
        return self._array_props_.get(idx, None)

    def _set_prop(self, name, value):
        idx = make_array_index(name)
        if idx != NOT_ARRAY_INDEX:
            self._set_iprop(idx, value)
        else:
            W_BasicObject._set_prop(self, name, value)

    def _set_iprop(self, idx, value):
        assert isinstance(idx, int)
        assert idx >= 0
        self._array_props_[idx] = value

    def _del_prop(self, name):
        idx = make_array_index(name)
        if idx != NOT_ARRAY_INDEX:
            self._del_iprop(idx)
        else:
            W_BasicObject._del_prop(self, name)

    def _del_iprop(self, idx):
        assert isinstance(idx, int)
        assert idx >= 0
        try:
            del self._array_props_[idx]
        except KeyError:
            pass

    def _named_properties_dict(self):
        my_d = {}
        for i in self._array_props_.keys():
            my_d[unicode(str(i))] = None

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

    def _get_idx_property(self, idx):
        prop = self._get_own_idx_property(idx)
        if prop is not None:
            return prop

        proto = self.prototype()
        if isnull(proto):
            return None

        if isinstance(proto, W__Array):
            return proto._get_idx_property(idx)

        assert isinstance(proto, W_BasicObject)
        p = unicode(str(idx))
        return proto.get_property(p)

    def w_get(self, w_p):
        if isinstance(w_p, W_IntNumber):
            idx = w_p.ToInteger()
            if idx >= 0:
                desc = self._get_idx_property(idx)
                return _get_from_desc(desc, self)

        return W_BasicObject.w_get(self, w_p)

    def w_put(self, w_p, v, throw=False):
        if isinstance(w_p, W_IntNumber):
            idx = w_p.ToInteger()
            if idx >= 0:
                self._idx_put(idx, v, throw)
                return

        W_BasicObject.w_put(self, w_p, v, throw)

    def _idx_put(self, idx, v, throw):
        d = self._can_idx_put(idx)
        can_put = d.can_put
        own_desc = d.own
        inherited_desc = d.inherited
        prop = d.prop

        if not can_put:
            if throw:
                raise JsTypeError(u"can't put %s" % (str(idx), ))
            else:
                return

        if is_data_descriptor(own_desc):
            value_desc = PropertyDescriptor(value=v)
            self._define_own_idx_property(idx, value_desc, throw, own_desc, prop)
            return

        if own_desc is None:
            desc = inherited_desc
        else:
            desc = own_desc

        if is_accessor_descriptor(desc):
            setter = desc.setter
            assert setter is not None
            setter.Call(this=self, args=[v])
        else:
            new_desc = DataPropertyDescriptor(v, True, True, True)
            self._define_own_idx_property(idx, new_desc, throw)

    def _can_idx_put(self, idx):
        prop = self._get_iprop(idx)

        if prop is None:
            desc = None
        else:
            desc = prop.to_property_descriptor()

        #desc = self._get_own_idx_property(idx)
        if desc is not None:
            if is_accessor_descriptor(desc) is True:
                if isundefined(desc.setter):
                    return Descr(False, desc, None, prop)
                else:
                    return Descr(True, desc, None, prop)
            return Descr(desc.writable, desc, None, prop)

        proto = self.prototype()

        if isnull_or_undefined(proto):
            return Descr(self.extensible(), None, None, prop)

        assert isinstance(proto, W_BasicObject)

        if isinstance(proto, W__Array):
            inherited = proto._get_idx_property(idx)
        else:
            p = unicode(str(idx))
            inherited = proto.get_property(p)

        if inherited is None:
            return Descr(self.extensible(), None, None, prop)

        if is_accessor_descriptor(inherited) is True:
            if isundefined(inherited.setter):
                return Descr(False, None, inherited, prop)
            else:
                return Descr(True, None, inherited, prop)
        else:
            if self.extensible() is False:
                return Descr(False, None, inherited, prop)
            else:
                return Descr(inherited.writable, None, inherited, prop)

    def _define_own_idx_property(self, idx, desc, throw=False, current_desc=None, prop=None):
        if current_desc is None:
            current_desc = self._get_idx_property(idx)

        old_len_desc = self.get_own_property(u'length')
        assert old_len_desc is not None
        old_len = old_len_desc.value.ToUInt32()

        # a
        index = idx
        # b
        if index >= old_len and old_len_desc.writable is False:
            return _ireject(throw, idx)

        # c
        succeeded = self._define_own_int_property(idx, desc, False, current_desc, prop)
        # d
        if succeeded is False:
            return _ireject(throw, idx)

        # e
        if index >= old_len:
            old_len_desc.value = _w(index + 1)
            res = W_BasicObject.define_own_property(self, u'length', old_len_desc, False)
            assert res is True
        # f
        return True

    def _define_own_int_property(self, idx, desc, throw, current_desc, prop):
        current = current_desc
        extensible = self.extensible()

        # 3.
        if current is None and extensible is False:
            return _ireject(throw, idx)

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
                self._add_iprop(idx, new_prop)
            # 4.b
            else:
                assert is_accessor_descriptor(desc) is True
                new_prop = AccessorProperty(
                    desc.getter,
                    desc.setter,
                    desc.enumerable,
                    desc.configurable
                )
                self._add_iprop(idx, new_prop)
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
                return _ireject(throw, idx)
            if desc.has_set_enumerable() and (not(current.enumerable) == desc.enumerable):
                return _ireject(throw, idx)

        # 8.
        if is_generic_descriptor(desc):
            pass
        # 9.
        elif is_data_descriptor(current) != is_data_descriptor(desc):
            # 9.a
            if current.configurable is False:
                return _ireject(throw, idx)
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
                    return _ireject(throw, idx)
                # 10.a.ii
                if current.writable is False:
                    if desc.has_set_value() and desc.value != current.value:
                        return _ireject(throw, idx)
            # 10.b
            else:
                pass
        # 11
        elif is_accessor_descriptor(current) and is_accessor_descriptor(desc):
            # 11.a
            if current.configurable is False:
                # 11.a.i
                if desc.has_set_setter() and desc.setter != current.setter:
                    return _ireject(throw, idx)
                # 11.a.ii
                if desc.has_set_getter() and desc.getter != current.getter:
                    return _ireject(throw, idx)
        # 12
        prop = self._get_iprop(idx)
        prop.update_with_descriptor(desc)

        # 13
        return True

    def _get_own_idx_property(self, idx):
        assert isinstance(idx, int)
        assert idx >= 0
        prop = self._get_iprop(idx)
        if prop is None:
            return

        return prop.to_property_descriptor()

    def define_own_property(self, p, desc, throw=False):
        if p == u'length':
            old_len_desc = self.get_own_property(u'length')
            assert old_len_desc is not None
            old_len = old_len_desc.value.ToUInt32()

            if desc.has_set_value() is False:
                return W_BasicObject.define_own_property(self, u'length', desc, throw)
            new_len_desc = desc.copy()
            new_len = desc.value.ToUInt32()

            if new_len != desc.value.ToNumber():
                raise JsRangeError()

            new_len_desc.value = _w(new_len)

            # f
            if new_len >= old_len:
                return W_BasicObject.define_own_property(self, u'length', new_len_desc, throw)
            # g
            if old_len_desc.writable is False:
                return reject(throw, p)

            # h
            if new_len_desc.has_set_writable() is False or new_len_desc.writable is True:
                new_writable = True
            # i
            else:
                new_writable = False
                new_len_desc.writable = True

            # j
            succeeded = W_BasicObject.define_own_property(self, u'length', new_len_desc, throw)
            # k
            if succeeded is False:
                return False

            # l
            while new_len < old_len:
                old_len = old_len - 1
                delete_succeeded = self.delete(unicode(str(old_len)), False)
                if delete_succeeded is False:
                    new_len_desc.value = _w(old_len + 1)
                    if new_writable is False:
                        new_len_desc.writable = False
                    W_BasicObject.define_own_property(self, u'length', new_len_desc, False)
                    return reject(throw, p)

            # m
            if new_writable is False:
                desc = PropertyDescriptor(writable=False)
                res = W_BasicObject.define_own_property(self, u'length', desc, False)
                assert res is True

            return True

        # 4
        elif is_array_index(p):
            index = uint32(int(p))
            return self._define_own_idx_property(index, desc, False)

        # 5
        return W_BasicObject.define_own_property(self, p, desc, throw)