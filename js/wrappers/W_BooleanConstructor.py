from js.wrappers.W_BasicFunction import W_BasicFunction


class W_BooleanConstructor(W_BasicFunction):
    def Call(self, args=[], this=None, calling_context=None):
        if len(args) >= 1 and not isnull_or_undefined(args[0]):
            boolval = args[0].to_boolean()
            return _w(boolval)
        else:
            return _w(False)

    def Construct(self, args=[]):
        return self.Call(args).ToObject()

    def _to_string_(self):
        return u'function Boolean() { [native code] }'