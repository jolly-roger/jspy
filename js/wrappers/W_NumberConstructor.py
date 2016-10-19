from js.wrappers.W_BasicFunction import W_BasicFunction


class W_NumberConstructor(W_BasicFunction):
    def Call(self, args=[], this=None, calling_context=None):
        if len(args) >= 1 and not isnull_or_undefined(args[0]):
            return _w(args[0].ToNumber())
        elif len(args) >= 1 and isundefined(args[0]):
            return _w(NAN)
        else:
            return _w(0.0)

    def Construct(self, args=[]):
        return self.Call(args).ToObject()

    def _to_string_(self):
        return u'function Number() { [native code] }'