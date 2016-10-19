from js.wrappers.W_BasicFunction import W_BasicFunction
from js.wrappers.W__Object import W__Object


class W_ObjectConstructor(W_BasicFunction):
    def Call(self, args=[], this=None, calling_context=None):
        value = get_arg(args, 0)

        if isinstance(value, W_BasicObject):
            return value
        if isinstance(value, W_String):
            return value.ToObject()
        if isinstance(value, W_Boolean):
            return value.ToObject()
        if isinstance(value, W_Number):
            return value.ToObject()

        assert isnull_or_undefined(value)

        obj = W__Object()
        return obj

    def _to_string_(self):
        return u'function Object() { [native code] }'

    # TODO
    def Construct(self, args=[]):
        return self.Call(args, this=None)