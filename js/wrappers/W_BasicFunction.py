from js.wrappers.W_BasicObject import W_BasicObject


class W_BasicFunction(W_BasicObject):
    _class_ = 'Function'
    _type_ = 'function'

    def Call(self, args=[], this=None, calling_context=None):
        raise NotImplementedError("abstract")

    def Construct(self, args=[]):
        proto = self.get(u'prototype')
        if isinstance(proto, W_BasicObject):
            obj = object_space.new_obj()
            object_space.assign_proto(obj, proto)
        else:
            # would love to test this
            # but I fail to find a case that falls into this
            obj = object_space.new_obj()

        result = self.Call(args, this=obj)
        if isinstance(result, W__Object):
            return result

        return obj

    def is_callable(self):
        return True

    def _to_string_(self):
        return u'function() {}'

    def has_instance(self, v):
        if not isinstance(v, W_BasicObject):
            return False

        o = self.get(u'prototype')

        if not isinstance(o, W_BasicObject):
            raise JsTypeError(u'has_instance')

        while True:
            assert isinstance(v, W_BasicObject)
            v = v.prototype()
            if isnull_or_undefined(v):
                return False
            if v == o:
                return True